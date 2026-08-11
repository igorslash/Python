"""
Модуль запросов: поиск + генерация ответа.

КЛЮЧЕВЫЕ РЕШЕНИЯ:
- Структурированный ответ (dataclass), а не сырая строка.
- response_mode="compact" для экономии токенов.
- Безопасное извлечение метаданных через .get().
"""
from __future__ import annotations

import logging
from dataclasses import dataclass  # dataclass для структурированного ответа. JSON-сериализуемый, типизированный, самодокументируемый.

from llama_index.core import VectorStoreIndex
from llama_index.core.base.response.schema import Response  # Тип ответа LlamaIndex. Содержит .response (str) и .source_nodes (list[NodeWithScore]).

from src.config import RAGConfig

logger = logging.getLogger(__name__)


@dataclass
class RAGResponse:
    """
    Структурированный ответ RAG-системы.

    ПОЧЕМУ НЕ ПРОСТО СТРОКА:
    - Frontend/API может напрямую сериализовать в JSON.
    - Источники отделены от ответа: UI может показать их отдельно.
    - Можно добавить поля (confidence, latency) без ломания контракта.
    - Тестировать проще: assert response.num_sources == 3.
    """
    answer: str  # Текст ответа LLM.
    sources: list[dict]  # Список источников с метаданными. dict, а не NodeWithScore, чтобы отвязать от LlamaIndex-типов.
    num_sources: int  # Количество источников. Удобно для логирования и UI без len(sources).


def ask(index: VectorStoreIndex, question: str, config: RAGConfig) -> RAGResponse:
    """
    Задать вопрос к индексу и получить структурированный ответ.

    Args:
        index: Загруженный VectorStoreIndex (уже с правильными эмбеддингами).
        question: Вопрос пользователя.
        config: Конфигурация (top_k, модель и т.д.).

    Returns:
        RAGResponse с ответом и источниками.
    """
    # === Создание QueryEngine ===
    engine = index.as_query_engine(
        similarity_top_k=config.similarity_top_k,  # Берём из конфига, а не хардкодим.
        response_mode="compact",  # Compact mode: LlamaIndex сжимает retrieved chunks, убирая нерелевантные части.
        # Экономит ~30% токенов и снижает риск галлюцинаций (меньше шума в контексте).
    )

    logger.info("Query: '%s' (top_k=%d)", question[:80], config.similarity_top_k)  # Логируем первые 80 символов вопроса. Полные вопросы могут содержать PII.

    # === Выполнение запроса ===
    response: Response = engine.query(question)  # engine.query() выполняет: retrieval → prompt assembly → LLM call → parsing.

    # === Извлечение источников ===
    sources = []
    for node in response.source_nodes:  # source_nodes — список NodeWithScore, упорядоченный по релевантности.
        sources.append({
            "file": node.metadata.get("file_name", "unknown"),  # .get() вместо ["file_name"]: предотвращает KeyError, если метаданные отсутствуют.
            "score": round(node.score, 4) if node.score else None,  # score может быть None для некоторых retriever'ов. round(4) — читаемость без потери точности.
            "snippet": node.get_content()[:150].replace("\n", " "),  # Первые 150 символов для превью. \n → пробел для однострочного вывода в CLI/UI.
        })

    result = RAGResponse(
        answer=str(response),  # str(response) извлекает текстовый ответ из Response-объекта.
        sources=sources,
        num_sources=len(sources),
    )

    logger.info(
        "Response generated: %d sources, answer length=%d chars",
        result.num_sources,
        len(result.answer),
    )
    return result