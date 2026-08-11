"""
Модуль индексации: загрузка → чанкинг → эмбеддинг → сохранение.

КЛЮЧЕВОЙ ПРИНЦИП:
Индекс строится ИЗ ЧАНКОВ (nodes), а не из сырых документов.
Это частая ошибка в туториалах: VectorStoreIndex(documents) игнорирует чанкинг.
"""
from __future__ import annotations

import logging  # logging вместо print. В продакшене print невозможно фильтровать по уровням, перенаправлять в файл или интегрировать с мониторингом.

from llama_index.core import (  # Импорт только core-компонентов. LlamaIndex v0.10+ разделил пакеты: core, embeddings-openai, llms-openai и т.д.
    Settings,  # Глобальный синглтон настроек. Все downstream-компоненты подхватывают автоматически.
    SimpleDirectoryReader,  # Загрузчик файлов. Поддерживает .txt, .md, .pdf, .docx из коробки.
    StorageContext,  # Контекст хранения: абстракция над тем, КАК сохраняется индекс (диск, S3, DB).
    VectorStoreIndex,  # In-memory векторный индекс. По умолчанию использует FAISS.
    load_index_from_storage,  # Загрузка ранее сохранённого индекса.
)
from llama_index.core.node_parser import SentenceSplitter  # SentenceSplitter разбивает текст по границам предложений. Это сохраняет семантику лучше, чем фиксированный размер символов.

from src.config import RAGConfig  # Импорт нашей конфигурации. Зависимость идёт внутрь, а не наружу.

logger = logging.getLogger(__name__)  # __name__ = "src.indexing". Позволяет фильтровать логи по модулю: видеть только логи индексации или все сразу.


def _configure_settings(config: RAGConfig) -> None:
    """
    Единая точка настройки глобальных Settings LlamaIndex.

    ПОЧЕМУ ОТДЕЛЬНАЯ ФУНКЦИЯ:
    - Настройки задаются ОДИН РАЗ. Нет риска использовать разные эмбеддинги
      при индексации и запросе (самая частая причина «мусорных» результатов).
    - QueryEngine, Retriever, Evaluator наследуют Settings автоматически.
    - Легко расширить: добавить reranker, callback manager и т.д. в одном месте.
    """
    # === Настройка эмбеддингов ===
    if config.embedding_provider == "openai":  # Условное переключение провайдера. Позволяет A/B-тестировать модели без изменения бизнес-логики.
        from llama_index.embeddings.openai import OpenAIEmbeddings  # Lazy import: загружается только если выбран OpenAI. Экономит память и время старта при использовании HF.
        Settings.embed_model = OpenAIEmbeddings(model=config.openai_embedding_model)
    else:
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding
        Settings.embed_model = HuggingFaceEmbedding(model_name=config.hf_embedding_model)

    # === Настройка LLM ===
    from llama_index.llms.openai import OpenAI
    Settings.llm = OpenAI(model=config.llm_model, temperature=config.temperature)

    # === Настройка чанкинга ===
    Settings.chunk_size = config.chunk_size  # Эти значения используются SentenceSplitter, если не переданы явно.
    Settings.chunk_overlap = config.chunk_overlap

    logger.info(
        "Settings configured: embed=%s (%s), llm=%s, chunk=%d/%d",
        config.embedding_provider,
        config.openai_embedding_model if config.embedding_provider == "openai" else config.hf_embedding_model,
        config.llm_model,
        config.chunk_size,
        config.chunk_overlap,
    )


def build_index(config: RAGConfig) -> VectorStoreIndex:
    """
    Полный пайплайн индексации.

    ПОРЯДОК ОПЕРАЦИЙ КРИТИЧЕН:
    1. validate() — fail-fast до любых затратных операций
    2. configure — единая точка настроек
    3. load — загрузка документов
    4. split — чанкинг ДО индексации
    5. index — построение из чанков
    6. persist — сохранение на диск
    """
    config.validate()  # Проверяем конфиг ДО загрузки. Если data_dir не существует, не тратим время на инициализацию моделей.
    _configure_settings(config)

    # === Шаг 1: Загрузка документов ===
    logger.info("Loading documents from %s", config.data_dir)
    reader = SimpleDirectoryReader(
        input_dir=str(config.data_dir),  # SimpleDirectoryReader принимает str, не Path. Поэтому str().
        recursive=True,  # Рекурсивный обход поддиректорий. Поддерживает вложенную структуру документации.
    )
    documents = reader.load_data()

    if not documents:  # Явная проверка. Без неё VectorStoreIndex([]) упадёт с загадочной ошибкой "No nodes to index".
        raise ValueError(f"No supported documents found in {config.data_dir}")

    logger.info("Loaded %d documents", len(documents))

    # === Шаг 2: Чанкинг ===
    splitter = SentenceSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
    )
    # get_nodes_from_documents — актуальный API. Старый get_chunks() устарел.
    # show_progress=True показывает tqdm-бар. Для больших датасетов пользователь видит прогресс, а не думает, что скрипт завис.
    nodes = splitter.get_nodes_from_documents(documents, show_progress=True)
    logger.info("Created %d chunks from %d documents", len(nodes), len(documents))

    # === Шаг 3: Создание индекса ИЗ ЧАНКОВ ===
    # VectorStoreIndex(nodes) — НЕ VectorStoreIndex(documents)!
    # Если передать documents, LlamaIndex применит дефолтный чанкинг из Settings,
    # а наш явный splitter будет проигнорирован.
    index = VectorStoreIndex(nodes, show_progress=True)

    # === Шаг 4: Сохранение ===
    config.persist_dir.mkdir(parents=True, exist_ok=True)  # Создаём директорию, если не существует. parents=True создаёт промежуточные папки.
    index.storage_context.persist(persist_dir=str(config.persist_dir))
    logger.info("Index saved to %s (%d vectors)", config.persist_dir, len(nodes))

    return index


def load_index(config: RAGConfig) -> VectorStoreIndex:
    """
    Загрузка ранее сохранённого индекса.

    ВАЖНО: _configure_settings вызывается и здесь!
    Эмбеддинги нужны для преобразования query в вектор при поиске.
    Если загрузить индекс с одними эмбеддингами, а искать другими —
    результаты будут бессмысленными (разные векторные пространства).
    """
    config.validate()
    _configure_settings(config)  # Те же эмбеддинги, что и при build_index. Гарантирует консистентность.

    storage_context = StorageContext.from_defaults(persist_dir=str(config.persist_dir))
    index = load_index_from_storage(storage_context)
    logger.info("Index loaded from %s", config.persist_dir)
    return index