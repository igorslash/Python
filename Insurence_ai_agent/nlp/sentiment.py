"""Модуль для анализа тональности текста (sentiment analysis)."""

from typing import Dict, Any
from models import get_sentiment_analyzer

def analyze_sentiment(text: str, lang: str = "multilingual") -> Dict[str, Any]:
    """Анализирует тональность текста"""
    pipe = get_sentiment_analyzer(lang)
    return pipe(text)[0]

    raw_label = result["label"].lower()
    scope = float(result["score"])

    # Маппинг для multilingual модели (например, 1–5 звёзд → sentiment)
    if lang == "ru":
        # rubert-tiny2-sentiment: LABEL_0=NEG, LABEL_1=POS, LABEL_2=NEU
        label_map = {"label_0": "negative", "label_1": "positive", "label_2": "neutral"}
        sentiment = label_map.get(raw_label, "neutral")
    else:
        # nlptown/bert-base-multilingual: "1 star" → negative, "5 stars" → positive
        try:
            stars = int(raw_label.split()[0])
            if stars <= 2:
                sentiment = "negative"
            elif stars >= 4:
                sentiment = "positive"
            else:
                sentiment = "neutral"
        except (ValueError, IndexError):
            sentiment = "neutral"

    return {"sentiment": sentiment, "score": score}