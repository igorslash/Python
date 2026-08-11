"""
Комплексная оценка RAG через RAGAS.

ПОЧЕМУ RAGAS, А НЕ РУЧНАЯ ОЦЕНКА:
- Автоматическая оценка через LLM-as-judge масштабируется на сотни вопросов.
- 4 метрики покрывают разные аспекты качества: галлюцинации, релевантность, ранжирование, полнота.
- Воспроизводимость: одни и те же данные → одни и те же результаты.

МЕТРИКИ:
- Faithfulness: ответ основан ТОЛЬКО на retrieved context (нет галлюцинаций).
- Answer Relevancy: ответ релевантен заданному вопросу.
- Context Precision: релевантные чанки ранжированы высоко в выдаче.
- Context Recall: все необходимые факты из ground_truth найдены в context.
"""
from __future__ import annotations

import asyncio  # async для параллельного выполнения запросов. 50 последовательных запросов = 5 мин, параллельно = ~40 сек.
import logging
from dataclasses import dataclass

from datasets import Dataset  # HuggingFace Dataset — формат данных, который ожидает RAGAS.
from langchain_openai import ChatOpenAI as LangChainChatOpenAI  # RAGAS использует LangChain-обёртки для LLM. Не путать с llama_index.llms.OpenAI.
from ragas import evaluate  # Основная функция оценки RAGAS.
from ragas.metrics import (  # Каждая метрика — отдельный класс. Можно добавлять/убирать без изменения остального кода.
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
    Faithfulness,
)

from src.config import RAGConfig
from src.indexing import load_index  # Загружаем тот же индекс, что используется в продакшене. Оценка должна быть на реальной системе.
from src.querying import ask  # Используем тот же ask(), что и в продакшене. Никаких специальных evaluation-only путей.

logger = logging.getLogger(__name__)


@dataclass
class EvalResult:
    """
    Результаты оценки. Dataclass для типизации и удобства.
    Все значения округлены до 4 знаков: 0.8765, а не 0.8765432109876543.
    """
    faithfulness: float
    answer_relevancy: float
    context_precision: float
    context_recall: float
    num_samples: int


# === Тестовый датасет ===
# В продакшене загружается из JSON/CSV/БД.
# ground_truth ОБЯЗАТЕЛЕН для ContextRecall.
# question + ground_truth должны быть составлены экспертом, а не сгенерированы LLM.
EVAL_DATASET = [
    {
        "question": "Как называется главный герой?",
        "ground_truth": "Главного героя зовут Александр Петров.",
    },
    {
        "question": "Какой протокол безопасности используется?",
        "ground_truth": "Система использует TLS 1.3 для всех входящих соединений.",
    },
    {
        "question": "Каков TTL токена аутентификации?",
        "ground_truth": "TTL токена составляет 3600 секунд.",
    },
    # ДОБАВЬТЕ МИНИМУМ 20-50 ПРИМЕРОВ ДЛЯ СТАТИСТИЧЕСКИ ЗНАЧИМЫХ РЕЗУЛЬТАТОВ.
    # 3 примера выше — только для демонстрации структуры.
]


async def run_evaluation(config: RAGConfig, dataset: list[dict] | None = None) -> EvalResult:
    """
    Запускает полную оценку RAG через RAGAS.

    ПРОЦЕСС:
    1. Для каждой пары (question, ground_truth) выполняется РЕАЛЬНЫЙ запрос к RAG.
    2. Собираются answer + retrieved contexts.
    3. RAGAS оценивает 4 метрики с помощью judge-LLM.

    ПОЧЕМУ ASYNC:
    RAGAS internally использует asyncio для параллельных LLM-вызовов.
    Наш внешний цикл тоже async, чтобы не блокировать event loop.

    Args:
        config: Конфигурация RAG (включая eval_llm_model).
        dataset: Тестовые данные. Если None — используется EVAL_DATASET.

    Returns:
        EvalResult с 4 метриками.
    """
    test_data = dataset or EVAL_DATASET

    if len(test_data) < 3:  # Предупреждение, а не ошибка. Позволяет запустить smoke-test с малым датасетом.
        logger.warning("Dataset too small (%d samples). Results may be unreliable.", len(test_data))

    # === Judge LLM ===
    # Judge ДОЛЖЕН быть сильнее генерирующей модели.
    # gpt-4o оценивает gpt-4o-mini. Если judge слабее, он не заметит ошибки слабой модели.
    judge_llm = LangChainChatOpenAI(
        model=config.eval_llm_model,
        temperature=0,  # Детерминированная оценка. Мы хотим воспроизводимость метрик.
    )

    # === Загрузка индекса и прогон реальных запросов ===
    index = load_index(config)  # Тот же индекс, что в продакшене.

    questions: list[str] = []
    answers: list[str] = []
    contexts: list[list[str]] = []  # RAGAS ожидает list[list[str]]: для каждого вопроса — список строк контекста.
    ground_truths: list[str] = []

    logger.info("Running %d queries against RAG system...", len(test_data))
    for item in test_data:
        result = ask(index, item["question"], config)  # Тот же ask(), что в продакшене. Никаких special-casing для оценки.
        questions.append(item["question"])
        answers.append(result.answer)
        contexts.append([s["snippet"] for s in result.sources])  # Извлекаем snippets из структурированного ответа.
        ground_truths.append(item["ground_truth"])

    # === Формирование Dataset для RAGAS ===
    # RAGAS требует строго определённые колонки: question, answer, contexts, ground_truth.
    ragas_dataset = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    })

    # === Определение метрик ===
    # Каждая метрика получает judge_llm. Можно использовать разные judge для разных метрик,
    # но обычно одна сильная модель достаточно.
    metrics = [
        Faithfulness(llm=judge_llm),        # Разбивает answer на atomic claims → проверяет каждый против contexts.
        AnswerRelevancy(llm=judge_llm),     # Генерирует потенциальные вопросы по answer → cosine similarity с исходным question.
        ContextPrecision(llm=judge_llm),    # Проверяет, ранжированы ли релевантные contexts выше нерелевантных.
        ContextRecall(llm=judge_llm),       # Сравнивает ground_truth с contexts. Проверяет полноту поиска.
    ]

    # === Запуск оценки ===
    logger.info("Evaluating with RAGAS (judge: %s, metrics: %d)...", config.eval_llm_model, len(metrics))
    results = evaluate(
        dataset=ragas_dataset,
        metrics=metrics,
    )

    # === Извлечение результатов ===
    scores = results.scores()  # Dict[str, float]: {"faithfulness": 0.91, "answer_relevancy": 0.88, ...}

    eval_result = EvalResult(
        faithfulness=round(scores["faithfulness"], 4),
        answer_relevancy=round(scores["answer_relevancy"], 4),
        context_precision=round(scores["context_precision"], 4),
        context_recall=round(scores["context_recall"], 4),
        num_samples=len(test_data),
    )

    logger.info(
        "Evaluation complete: Faith=%.4f | AnsRel=%.4f | CtxPrec=%.4f | CtxRec=%.4f (n=%d)",
        eval_result.faithfulness, eval_result.answer_relevancy,
        eval_result.context_precision, eval_result.context_recall,
        eval_result.num_samples,
    )

    return eval_result