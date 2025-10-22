"""Модуль для детекции языка входного текста."""
from langdetect import detect, LangDetectException

def detect_language(text: str) -> str:
    """Детектирует язык входного текста.

    :param text: входной текст
    :return: язык текста
    """
    try:
        lang = detect(text)
        return lang
    except LangDetectException as e:
        raise ValueError(f"Не удалось определить язык текста: {e}")