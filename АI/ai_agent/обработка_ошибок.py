from transformers import AutoTokenizer, AutoModel
import torch
from typing import Dict, Any, Optional

_MODEL_CACHE = {}


def get_embeddings(text: str, model_name: str = "bert-base-uncased") -> Optional[Dict[str, Any]]:
    """Получает эмбеддинги текста с помощью BERT."""

    # ← ДОБАВИЛИ ПРОВЕРКИ
    if not text or not text.strip():
        print("❌ Ошибка: Пустой текст")
        return None

    try:
        if model_name not in _MODEL_CACHE:
            print(f"🔄 Загружаем модель {model_name}...")
            _MODEL_CACHE[model_name] = {
                'tokenizer': AutoTokenizer.from_pretrained(model_name),
                'model': AutoModel.from_pretrained(model_name)
            }

        tokenizer = _MODEL_CACHE[model_name]['tokenizer']
        model = _MODEL_CACHE[model_name]['model']

        inputs = tokenizer(text, return_tensors="pt", truncation=True,
                           padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)

        return {
            "embeddings": outputs.last_hidden_state.tolist(),
            "shape": list(outputs.last_hidden_state.shape),
            "model": model_name,
            "text_length": len(text)
        }

    # ← ДОБАВИЛИ ОБРАБОТКУ ОШИБОК
    except Exception as e:
        print(f"❌ Ошибка при обработке текста: {e}")
        return None


# Теперь код устойчив к ошибкам!
result1 = get_embeddings("")  # Пустой текст → ошибка
result2 = get_embeddings("Hello world")  # Успех
result3 = get_embeddings("x" * 1000)  # Длинный текст → обрежется