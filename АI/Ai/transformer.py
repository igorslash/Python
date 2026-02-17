import torch
from transformers import BertModel, BertTokenizer

# 1. Загрузка модели и токенизатора
model = BertModel.from_pretrained("bert-base-cased")
tokenizer = BertTokenizer.from_pretrained("bert-base-cased")

# 2. Определение входной последовательности
sequence = "Hello, my dog is cute"

# 3. Токенизация входной последовательности
# Преобразование текста в числовые идентификаторы (токены)
# и добавление специальных токенов
inputs = tokenizer(sequence, return_tensors="pt")

# 4. Передача токенов в модель
outputs = model(**inputs)

# 5. Извлечение скрытых состояний последнего слоя
last_hidden_states = outputs.last_hidden_state

# 6. Вывод результата
print("Входные токены (отображение токенов на "
      "их числовые идентификаторы):")
print(inputs)
print("\nПоследние скрытые состояния (эмбеддинги):")
print(last_hidden_states)
print("\nРазмерность тензора скрытых состояний (batch_size, "
      "sequence_length, hidden_size):")
print(last_hidden_states.shape)
