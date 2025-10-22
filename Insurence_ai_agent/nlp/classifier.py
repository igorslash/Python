"""Модуль для классификации типов обращений клиентов."""
from typing import Dict, Any
from models import get_classifier

def classify_support_request(text: str, lang: str = "multilingual") -> Dict[str, Any]:
    """Классифицирует текст обращения в поддержку"""
    pipe = get_classifier(lang)
    result = pipe(text)[0] # берем самый вероятный результат

    # Нормализуем метку: приводим к нижнему регистру и убираем префиксы
    label = result["label"].lower()
    if "insurance" in label or "insurance" in label:
        label = "insurance"
    elif "support" in label or "техпод" in label:
        label = "support"
    elif "complaint" in label or "жалоб" in label:
        label = "complaint"
    else:
        label = "other"

    return {
        "label": label,
        "score": float(result["score"]),
    }