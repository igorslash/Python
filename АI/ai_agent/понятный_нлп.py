from transformers import AutoTokenizer, AutoModel
import torch

# 1. Загружаем токенизатор и модель
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# 2. Подготавливаем текст
text = "Hello, I'm learning NLP!"
inputs = tokenizer(text, return_tensors="pt")

# 3. Прямой проход (инференс)
with torch.no_grad():
    outputs = model(**inputs)

# 4. Смотрим результат
print("Форма выхода:", outputs.last_hidden_state.shape)

