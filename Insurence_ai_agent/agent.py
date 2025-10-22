"""Основной AI-агент для обработки страховых запросов и NLP-задач."""

from typing import Dict, Any, Optional, List
from nlp.language import detect_language
from nlp.classifier import classify_support_request
from nlp.sentiment import analyze_sentiment
from nlp.ner import extract_entities
from nlp.recommender import recommend_insurance


class InsuranceAgent:
    """AI-агент для обработки клиентских запросов в сфере страхования."""

    def __init__(self) -> None:
        pass

    def process(
        self,
        text: str,
        task_type: Optional[str] = None,
        profile: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not text.strip():
            raise ValueError("Входной текст не может быть пустым.")

        # 1. Определяем язык
        try:
            lang = detect_language(text)
        except ValueError as e:
            raise ValueError(f"Ошибка детекции языка: {e}")

        # 2. Определяем тип задачи
        if task_type is None:
            task_type = self._infer_task_type(text)

        # 3. Выполняем задачу
        if task_type == "support_classification":
            result = classify_support_request(text, lang=lang)
        elif task_type == "sentiment_analysis":
            result = analyze_sentiment(text, lang=lang)
        elif task_type == "ner":
            result = extract_entities(text, lang=lang)
        elif task_type == "insurance_recommendation":
            entities = extract_entities(text, lang=lang)["entities"]
            if profile is None:
                # Простой fallback: извлекаем возраст и цели из текста
                profile = self._build_profile_from_text(text, entities)
            result = recommend_insurance(profile=profile, entities=entities)
        else:
            raise ValueError(f"Неизвестный тип задачи: {task_type}")

        return {
            "task": task_type,
            "result": result,
            "language": lang,
        }

    def _infer_task_type(self, text: str) -> str:
        """автоматически определиям тип задачи по тексту."""
        text_lower = text.lower()
        support_keywords = ["поддержка", "техподдержка", "help", "support"]
        sentiment_keywords = ["отзыв", "мнение", "review", "feel", "оценка"]
        ner_keywords = ["документ", "паспорт", "дата", "сумма", "договор", "document"]
        insurance_keywords = [
            "страх", "полис", "страховка", "тариф", "insurance", "policy", "quote"
        ]

        if any(kw in text_lower for kw in insurance_keywords):
            return "insurance_recommendation"
        if any(kw in text_lower for kw in support_keywords):
            return "support_classification"
        if any(kw in text_lower for kw in sentiment_keywords):
            return "sentiment_analysis"
        if any(kw in text_lower for kw in ner_keywords):
            return "ner"

        return "support_classification"

    def _build_profile_from_text(
        self, text: str, entities: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Создаёv временный профиль клиента на основе текста и сущностей."""
        age = 30
        for ent in entities:
            if ent["label"] in ("AGE", "NUMBER") and ent["text"].isdigit():
                candidate = int(ent["text"])
                if 10 <= candidate <= 100:
                    age = candidate
                    break

        # Определяем цели по ключевым словам
        goals = []
        text_lower = text.lower()
        if any(kw in text_lower for kw in ["авто", "car", "осаго"]):
            goals.append("auto")
        if any(kw in text_lower for kw in ["здоровье", "health", "медицин"]):
            goals.append("health")
        if any(kw in text_lower for kw in ["путешеств", "travel", "поездк"]):
            goals.append("travel")

        return {"age": age, "goals": goals}