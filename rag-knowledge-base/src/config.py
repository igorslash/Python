"""
Централизованная конфигурация RAG-системы.

ПОЧЕМУ ОТДЕЛЬНЫЙ МОДУЛЬ:
- Все настройки в одном месте, а не разбросаны по коду.
- Переключение между окружениями (dev/prod) без изменения кода.
- Fail-fast валидация: ошибки ловятся на старте, а не через 30 минут индексации.
"""

from __future__ import annotations  # Позволяет использовать тип RAGConfig внутри самого класса RAGConfig (forward reference). Без этого в Python <3.11 была бы ошибка NameError.

import os  # Стандартная библиотека для чтения переменных окружения.
from dataclasses import dataclass  # dataclass автоматически генерирует __init__, __repr__, __eq__. Меньше бойлерплейта, меньше шансов на ошибку.
from pathlib import Path  # Path удобнее str для работы с путями: поддерживает /, .exists(), .mkdir() и т.д.


@dataclass(frozen=True)  # frozen=True делает объект иммутабельным. После создания нельзя случайно изменить chunk_size посередине пайплайна. Это принцип defensive programming.
class RAGConfig:
    """
    Immutable-конфигурация RAG-системы.
    Все значения читаются из env с безопасными дефолтами.
    Система работает «из коробки» для разработки, но полностью настраивается для продакшена.
    """

    # === Пути ===
    data_dir: Path = Path(os.getenv("RAG_DATA_DIR", "data"))  # Папка с исходными документами. Дефолт "data" — стандартное соглашение.
    persist_dir: Path = Path(os.getenv("RAG_PERSIST_DIR", "index"))  # Папка для сохранения FAISS-индекса. Отделена от данных, чтобы можно было бэкапить/версионировать независимо.

    # === Чанкинг ===
    chunk_size: int = int(os.getenv("RAG_CHUNK_SIZE", "1000"))  # Размер чанка в символах. 1000 — баланс между контекстом и точностью поиска. int() нужен, потому что getenv возвращает str.
    chunk_overlap: int = int(os.getenv("RAG_CHUNK_OVERLAP", "200"))  # Перекрытие чанков. 20% от chunk_size — эмпирический оптимум: достаточно для сохранения контекста на стыках, но не дублирует слишком много.

    # === Эмбеддинги ===
    embedding_provider: str = os.getenv("RAG_EMBEDDING_PROVIDER", "openai")  # Провайдер эмбеддингов. Поддержка нескольких провайдеров позволяет тестировать локальные модели без затрат на API.
    openai_embedding_model: str = os.getenv("RAG_OPENAI_EMBED_MODEL", "text-embedding-3-small")  # text-embedding-3-small: лучшее соотношение цена/качество для большинства задач.
    hf_embedding_model: str = os.getenv("RAG_HF_EMBED_MODEL", "intfloat/multilingual-e5-large")  # Fallback для офлайн-работы или когда данные нельзя отправлять в облако.

    # === LLM для генерации ===
    llm_model: str = os.getenv("RAG_LLM_MODEL", "gpt-4o-mini")  # gpt-4o-mini: достаточно умная для RAG, но дешёвая. Для продакшена можно переключить на gpt-4o через env.
    temperature: float = float(os.getenv("RAG_TEMPERATURE", "0"))  # temperature=0 делает ответы детерминированными. Для RAG это критично: мы хотим факты, а не креативность.

    # === Поиск ===
    similarity_top_k: int = int(os.getenv("RAG_TOP_K", "3"))  # Количество возвращаемых чанков. 3 — компромисс между полнотой и шумом. Больше k = больше контекста, но выше риск нерелевантных чанков.

    # === LLM для оценки (Judge) ===
    eval_llm_model: str = os.getenv("RAG_EVAL_LLM_MODEL", "gpt-4o")  # Judge ДОЛЖЕН быть сильнее генерирующей модели. gpt-4o оценивает gpt-4o-mini. Если judge слабее, он не заметит ошибки.

    def validate(self) -> None:
        """
        Fail-fast валидация конфигурации.
        Вызывается при старте, а не во время индексации/запроса.
        Экономит время и деньги: лучше упасть сразу, чем после 30 минут работы.
        """
        if self.chunk_overlap >= self.chunk_size:  # overlap >= size бессмыслен: чанки будут полностью дублировать друг друга.
            raise ValueError(
                f"chunk_overlap ({self.chunk_overlap}) must be < chunk_size ({self.chunk_size})"
            )
        if self.similarity_top_k < 1:  # top_k=0 вернёт пустой результат, что сломает downstream.
            raise ValueError(f"similarity_top_k must be >= 1, got {self.similarity_top_k}")
        if not self.data_dir.exists():  # Проверяем существование ДО загрузки. SimpleDirectoryReader вернёт пустой список без ошибки, и индексация упадёт с непонятным сообщением.
            raise FileNotFoundError(
                f"Data directory not found: {self.data_dir}. Create it and add documents."
            )