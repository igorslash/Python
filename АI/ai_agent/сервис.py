"""Сервис для получения текстовых эмбеддингов."""

from transformers import AutoTokenizer, AutoModel
import torch
from typing import Dict, Any, Optional
import logging
from functools import lru_cache  # ← ДОБАВИЛИ ДЕКОРАТОР

logger = logging.getLogger(__name__)


class EmbeddingService:  # ← ДОБАВИЛИ КЛАСС!
    """Сервис для работы с текстовыми эмбеддингами."""

    def __init__(self, default_model: str = "bert-base-uncased",
                 max_length: int = 512):
        self.default_model = default_model
        self.max_length = max_length
        self._models = {}
        logger.info(f"Инициализирован EmbeddingService с моделью "
                    f"{default_model}")

    @lru_cache(maxsize=10)  # ← ДОБАВИЛИ КЭШ ДЛЯ ТЕКСТОВ
    def get_embeddings(
            self,
            text: str,
            model_name: str = None,
            use_cache: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Получает эмбеддинги для текста."""

        model_name = model_name or self.default_model

        if not text or not text.strip():
            logger.warning("Получен пустой текст")
            return None

        try:
            # Загрузка модели если нужно
            if model_name not in self._models:
                logger.info(f"Загрузка модели: {model_name}")
                self._models[model_name] = {
                    'tokenizer': AutoTokenizer
                    .from_pretrained(model_name),
                    'model': AutoModel.from_pretrained(model_name)
                }

            tokenizer = self._models[model_name]['tokenizer']
            model = self._models[model_name]['model']

            # Токенизация
            inputs = tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=self.max_length
            )

            # Инференс
            with torch.no_grad():
                outputs = model(**inputs)

            # Формирование ответа
            return {
                "embeddings": outputs.last_hidden_state.tolist(),
                "shape": list(outputs.last_hidden_state.shape),
                "model": model_name,
                "text_length": len(text),
                "tokens_count": inputs["input_ids"].shape[1]
            }

        except Exception as e:
            logger.error(f"Ошибка обработки текста: {e}",
                         exc_info=True)
            return None


# ← ДОБАВИЛИ ГОТОВЫЙ ИНСТАНС ДЛЯ ИМПОРТА
default_embedding_service = EmbeddingService()

# Использование (теперь очень просто!)
from embedding_service import default_embedding_service

result = default_embedding_service.get_embeddings("Hello, production!")
print(result)