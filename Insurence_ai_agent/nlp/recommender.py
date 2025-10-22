"""Модуль для подбора персональных страховых решений."""

from typing import Dict, Any, List

_INSURANCE_PRODUCTS = [
    {
        "id": "auto_osago_1",
        "name": "ОСАГО Стандарт",
        "description": "Обязательное автострахование гражданской ответственности.",
        "target": "auto",
        "min_age": 18,
        "max_age": 75,
        "price_range": (3000, 7000),
        "currency": "RUB",
    },
    {
        "id": "health_premium_1",
        "name": "Здоровье Премиум",
        "description": "Расширенное медицинское страхование с покрытием стоматологии.",
        "target": "health",
        "min_age": 0,
        "max_age": 65,
        "price_range": (15000, 40000),
        "currency": "RUB",
    },
    {
        "id": "travel_eu_1",
        "name": "Путешествия в ЕС",
        "description": "Страховка для поездок в страны Шенгена.",
        "target": "travel",
        "min_age": 0,
        "max_age": 80,
        "price_range": (1500, 5000),
        "currency": "RUB",
    },
]


def recommend_insurance(
    profile: Dict[str, Any],
    entities: List[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Рекомендует страховой продукт на основе профиля клиента"""
    age = profile.get("age", 30)
    goals = profile.get("goals", [])
    if not goals:
        goals = _infer_goals_from_entities(entities)

    suitable = []
    for prod in _INSURANCE_PRODUCTS:
        if (
            prod["min_age"] <= age <= prod["max_age"]
            and prod["target"] in goals
        ):
            suitable.append(prod)

    if not suitable:
        return {
            "product": None,
            "reason": "Не найдено подходящих продуктов по вашему профилю.",
            "alternatives": [],
        }

    # Выбираем первый как основной (в реальности — по приоритету/цене)
    main = suitable[0]
    alternatives = suitable[1:3]

    return {
        "product": main,
        "reason": f"Рекомендуем {main['name']} для цели '{main['target']}'.",
        "alternatives": alternatives,
    }


def _infer_goals_from_entities(entities: List[Dict[str, Any]] = None) -> List[str]:
    if not entities:
        return []
    goal_map = {
        "авто": "auto",
        "машина": "auto",
        "здоровье": "health",
        "медицин": "health",
        "путешеств": "travel",
        "поездк": "travel",
        "car": "auto",
        "health": "health",
        "travel": "travel",
    }
    text = " ".join(ent["text"].lower() for ent in entities)
    goals = []
    for keyword, target in goal_map.items():
        if keyword in text and target not in goals:
            goals.append(target)
    return goals