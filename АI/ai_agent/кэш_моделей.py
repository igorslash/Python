from transformers import AutoTokenizer, AutoModel
import torch
from typing import Dict, Any  # ← ДОБАВИЛИ


def get_embeddings(text: str) -> Dict[str, Any]:  # ← ДОБАВИЛИ ФУНКЦИЮ
    """Получает эмбеддинги текста с помощью BERT."""
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)  # ← УЛУЧШИЛИ
    with torch.no_grad():
        outputs = model(**inputs)

    # Структурируем выход
    return {
        "embeddings": outputs.last_hidden_state.tolist(),
        "shape": list(outputs.last_hidden_state.shape),
        "model": model_name
    }


# Использование
result = get_embeddings("Hello, I'm learning NLP!")
print(result)