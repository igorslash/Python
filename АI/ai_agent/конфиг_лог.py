from transformers import AutoTokenizer, AutoModel
import torch
from typing import Dict, Any, Optional
import logging  # ← ДОБАВИЛИ ЛОГГИРОВАНИЕ

# ← ДОБАВИЛИ КОНФИГУРАЦИЮ
CONFIG = {
    "default_model": "bert-base-uncased",
    "max_length": 512,
    "cache_models": True
}

# ← ДОБАВИЛИ ЛОГГЕР
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_MODEL_CACHE = {}


def get_embeddings(
        text: str,
        model_name: str = None,
        return_tensors: bool = False  # ← ДОБАВИЛИ ОПЦИИ
) -> Optional[Dict[str, Any]]:
    """Получает эмбеддинги текста с помощью BERT."""

    if model_name is None:
        model_name = CONFIG["default_model"]

    if not text or not text.strip():
        logger.error("Пустой текст в запросе")
        return None

    try:
        if CONFIG["cache_models"] and model_name not in _MODEL_CACHE:
            logger.info(f"Загрузка модели {model_name}")
            _MODEL_CACHE[model_name] = {
                'tokenizer': AutoTokenizer.from_pretrained(model_name),
                'model': AutoModel.from_pretrained(model_name)
            }

        tokenizer = _MODEL_CACHE[model_name]['tokenizer']
        model = _MODEL_CACHE[model_name]['model']

        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=CONFIG["max_length"]
        )

        with torch.no_grad():
            outputs = model(**inputs)

        result = {
            "shape": list(outputs.last_hidden_state.shape),
            "model": model_name,
            "text_length": len(text)
        }

        # ← ДОБАВИЛИ ВЫБОР ФОРМАТА ВОЗВРАТА
        if return_tensors:
            result["embeddings"] = outputs.last_hidden_state
        else:
            result["embeddings"] = outputs.last_hidden_state.tolist()

        logger.info(f"Успешно обработан текст длиной {len(text)}")
        return result

    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)
        return None


# Профессиональное использование!
result = get_embeddings(
    text="Hello, professional NLP!",
    model_name="bert-base-uncased",
    return_tensors=False
)