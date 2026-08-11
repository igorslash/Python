"""
CLI для RAG-системы.

ПОЧЕМУ ARGPARSE, А НЕ INPUT():
- Скриптыруемый: можно вызвать из CI/CD, Makefile, cron.
- Самодокументируемый: --help показывает все команды.
- Расширяемый: легко добавить новые подкоманды.
"""
import argparse  # Стандартная библиотека для CLI. Не требует внешних зависимостей.
import asyncio  # run_evaluation — async функция. asyncio.run() запускает её в event loop.
import logging

from src.config import RAGConfig
from src.evaluation import run_evaluation
from src.indexing import build_index, load_index
from src.querying import ask


def setup_logging() -> None:
    """
    Настройка логирования.
    Вызывается один раз при старте.
    format включает timestamp, level, module name — достаточно для отладки и продакшена.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main() -> None:
    setup_logging()
    config = RAGConfig()  # Конфигурация создаётся один раз и передаётся во все функции.

    # === Парсинг аргументов ===
    parser = argparse.ArgumentParser(description="RAG Evaluation Pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)  # required=True: без команды покажет help, а не упадёт с AttributeError.

    subparsers.add_parser("build", help="Build index from documents in data/")
    subparsers.add_parser("load", help="Verify index loads correctly")

    ask_parser = subparsers.add_parser("ask", help="Ask a question to the RAG system")
    ask_parser.add_argument("question", type=str, help="Question to ask")  # Позиционный аргумент. type=str обеспечивает валидацию.

    subparsers.add_parser("eval", help="Evaluate RAG quality with RAGAS (4 metrics)")

    args = parser.parse_args()

    # === Диспетчеризация команд ===
    if args.command == "build":
        build_index(config)

    elif args.command == "load":
        load_index(config)
        print("✅ Index loaded successfully")  # print допустим для user-facing сообщений. Логирование — для системных событий.

    elif args.command == "ask":
        index = load_index(config)
        result = ask(index, args.question, config)
        print(f"\n💬 {result.answer}")
        print(f"\n📚 Sources ({result.num_sources}):")
        for i, source in enumerate(result.sources, 1):
            print(f"  {i}. [{source['file']}] (score={source['score']}) {source['snippet']}...")

    elif args.command == "eval":
        # asyncio.run() создаёт event loop, выполняет coroutine и закрывает loop.
        # Это единственный правильный способ запустить async из sync main().
        result = asyncio.run(run_evaluation(config))
        print("\n📊 RAG Evaluation Results:")
        print(f"  Faithfulness:      {result.faithfulness:.4f}")
        print(f"  Answer Relevancy:  {result.answer_relevancy:.4f}")
        print(f"  Context Precision: {result.context_precision:.4f}")
        print(f"  Context Recall:    {result.context_recall:.4f}")
        print(f"  Samples:           {result.num_samples}")


if __name__ == "__main__":  # Стандартный guard. Код выполняется только при прямом запуске, не при импорте.
    main()