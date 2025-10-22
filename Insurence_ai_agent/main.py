"""CLI-интерфейс для запуска Insurance AI Agent из командной строки.

Примеры использования:
    python main.py --text "Хочу страховку на авто, мне 35 лет"
    python main.py --text "Отличный сервис!" --task sentiment_analysis
    python main.py --text "Обратился в поддержку — не отвечают." --task support_classification
"""

import argparse
import json
import sys
from agent import InsuranceAgent


def main() -> None:
    """Запускает агент с параметрами из командной строки."""
    parser = argparse.ArgumentParser(
        description="AI-агент для обработки страховых запросов и NLP-анализа."
    )
    parser.add_argument(
        "--text",
        type=str,
        required=True,
        help="Входной текст от пользователя (обязательный)."
    )
    parser.add_argument(
        "--task",
        type=str,
        choices=[
            "support_classification",
            "sentiment_analysis",
            "ner",
            "insurance_recommendation",
        ],
        help=(
            "Тип задачи (опционально). Если не указан, "
            "агент попытается определить автоматически."
        ),
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Возраст клиента (для рекомендаций, по умолчанию: 30)."
    )
    parser.add_argument(
        "--goals",
        type=str,
        default="",
        help=(
            "Цели клиента через запятую (например: auto,health). "
            "Используется только при task=insurance_recommendation."
        ),
    )

    args = parser.parse_args()

    # Собираем профиль, если требуется
    profile = None
    if args.task == "insurance_recommendation" or "страх" in args.text.lower():
        goals = [g.strip() for g in args.goals.split(",")] if args.goals else []
        profile = {"age": args.age, "goals": goals}

    # Запуск агента
    agent = InsuranceAgent()
    try:
        result = agent.process(text=args.text, task_type=args.task, profile=profile)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

    # Вывод в формате JSON (удобен для интеграции с чат-ботом)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()