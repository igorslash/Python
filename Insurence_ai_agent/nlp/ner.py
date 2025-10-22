"""Модуль для извлечения именованных сущностей (NER) из текста."""

from typing import Dict, List, Any
from models import get_ner_pipeline


def extract_entities(text: str, lang: str = "multilingual") -> Dict[str, List[Dict[str, Any]]]:
    """Извлекает именованные сущности из текста"""

    pipe = get_ner_pipeline(lang)
    raw_entities = pipe(text)

    # Фильтруем и нормализуем
    entities = []
    for ent in raw_entities:
        entities.append({
            "text": ent["word"],
            "label": ent["entity_group"],
            "score": float(ent["score"]),
        })

    return {"entities": entities}