from typing import Dict

from transformers import pipeline

# Глобальный кэш пайплайнов (для избежания повторной загрузки)
_MODEL_CACHE: Dict[str, pipeline] = {}


def get_classifier(lang: str = "multilingual") -> pipeline:
    """Возвращает пайплайн для классификации обращений."""
    key = f"classifier_{lang}"
    if key not in _MODEL_CACHE:
        if lang == "ru":
            model_name = "cointegrated/rubert-tiny2-sentiment"
        else:
            # multilingual fallback
            model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
        _MODEL_CACHE[key] = pipeline("text-classification", model=model_name)
    return _MODEL_CACHE[key]

def get_sentiment_analyzer(lang: str = "multilingual") -> pipeline:
    """Возвращает пайплайн для анализа тональности."""
    # Используем ту же модель, что и для классификации, или отдельную при необходимости
    return get_classifier(lang)

def get_ner_pipeline(lang: str = "multilingual") -> pipeline:
    """Возвращает пайплайн для извлечения сущностей."""
    key = f"ner_{lang}"
    if key not in _MODEL_CACHE:
        if lang == "ru":
            model_name = "Davlan/bert-base-multilingual-cased-ner-hrl"
        else:
            model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
        _MODEL_CACHE[key] = pipeline("ner", model=model_name, aggregation_strategy="simple")
    return _MODEL_CACHE[key]