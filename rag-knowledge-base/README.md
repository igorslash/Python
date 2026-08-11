# RAG-Knowledge-Base

Production-ready RAG-система для поиска по корпоративной документации с комплексной автоматической оценкой качества через RAGAS.

## 🎯 Ключевые особенности

- **4 метрики RAGAS**: Faithfulness, Answer Relevancy, Context Precision, Context Recall
- **Judge ≠ Generator**: оценка моделью gpt-4o, генерация — gpt-4o-mini (надёжное детектирование галлюцинаций)
- **Модульная архитектура**: разделение ответственности на config / indexing / querying / evaluation
- **Fail-fast валидация**: ошибки конфигурации обнаруживаются на старте, а не после получаса индексации
- **Структурированные ответы**: `RAGResponse` dataclass вместо сырых строк — готово к API/JSON
- **Async-оценка**: параллельный прогон 50 тестовых запросов за ~40 секунд вместо 5 минут

## 🏗️ Архитектура

Documents ──▶ SentenceSplitter ──▶ Embeddings ──▶ FAISS Index
│
Question ──▶ Retriever (top-k) ──▶ Compact Prompt ──▶ LLM ──▶ Answer
│ │
▼ ▼
Retrieved Contexts RAGAS Judge (gpt-4o)
│ │
├──── Faithfulness ◀────────┤
├──── Answer Relevancy ◀────┤
├──── Context Precision ◀───┤
└──── Context Recall ◀──────┘

## 🚀 Запуск

### Установка

```bash
pip install -e .
cp .env.example .env
# Заполните OPENAI_API_KEY в .env

# Создайте тестовые данные
mkdir -p data
# Скопируйте ваши .txt / .md / .pdf файлы в data/

# Использование
# Построить индекс
python main.py build

# Задать вопрос
python main.py ask "Какой протокол безопасности используется?"

# Оценить качество (4 метрики RAGAS)
python main.py eval

# Проверить загрузку индекса
python main.py load


#структура проекта
src/
├── config.py         # Frozen dataclass + fail-fast validation
├── indexing.py       # Load → Split → Embed → Persist
├── querying.py       # Structured RAGResponse with sources
└── evaluation.py     # RAGAS: Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall
main.py               # CLI: build / ask / eval / load
.env.example          # Шаблон переменных (без секретов)
pyproject.toml        # Зависимости и мета-данные

#метрики 
 Метрики оценки
Метрика
Описание
Хорошее значение
Faithfulness
Доля утверждений в ответе, подтверждённых retrieved context. 1.0 = нет галлюцинаций
≥ 0.85
Answer Relevancy
Насколько ответ соответствует заданному вопросу. Штрафует за избыточную/неуместную информацию
≥ 0.80
Context Precision
Ранжирует ли ретривер релевантные чанки выше нерелевантных
≥ 0.75
Context Recall
Какая доля фактов из ground_truth присутствует в retrieved context
≥ 0.70

#зависимости
📦 Зависимости
LlamaIndex ≥0.12 — RAG-фреймворк
RAGAS ≥0.2 — оценка качества RAG
OpenAI — эмбеддинги и LLM
LangChain OpenAI — judge-обёртка для RAGAS
HuggingFace Datasets — формат данных для RAGAS
python-dotenv — загрузка .env


📦 Технические характеристики
Технологические решения
SentenceSplitter
Разбиение по границам предложений сохраняет семантику лучше, чем фиксированный размер символов
response_mode="compact"
Сжатие контекста перед отправкой в LLM снижает token usage на ~30% и уменьшает галлюцинации
Frozen dataclass config
Предотвращает runtime-мутацию настроек между индексацией и запросами
Lazy imports эмбеддингов
Загружается только выбранный провайдер. Экономит память и время старта
logging вместо print
Фильтрация по уровням, перенаправление в файл, интеграция с мониторингом
Async evaluation
Параллельные LLM-вызовы ускоряют прогон 50 примеров в 5–10 раз
RAGAS over manual eval
Автоматическая LLM-as-judge оценка масштабируется на сотни вопросов без ручной разметки