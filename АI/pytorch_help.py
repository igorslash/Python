#1. База: Тензоры и Устройство
import torch

# Создание тензора (обязательно float32 для нейронок)
x = torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float32)

# Выбор устройства (Автоматика для 4070 или Mac M4)
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

# Перенос на видеокарту (Сковородка и яйца должны быть в одном месте!)
x = x.to(device)
model = model.to(device)

# Главная команда для отладки (размерности):
print(x.shape) # Выдаст [Batch, Features], например [32, 768]

#-------------------------------------------------------------------
#2. Архитектура (Конструктор LEGO)
import torch.nn as nn

class MyNet(nn.Module):
    def __init__(self):
        super().__init__()
        # Вход предыдущего = Выход текущего!
        self.flatten = nn.Flatten()
        self.block = nn.Sequential(
            nn.Linear(28*28, 512), # 784 на входе
            nn.ReLU(),              # Нелинейность (изгиб пространства)
            nn.Dropout(0.2),        # Защита от зубрежки (переобучения)
            nn.Linear(512, 10)      # 10 классов на выходе (Логиты!)
        )

    def forward(self, x):
        x = self.flatten(x)
        return self.block(x)
#-------------------------------------------------------------------
#3. Обучение (Строитель)
model = MyNet()
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)# Настройка
# скорости обучения Adam  (AdamW)
for epoch in range(10):
    for batch in train_loader:
        x, y = batch
        pred = model(x)
        loss = loss_fn(pred, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print(f"Epoch: {epoch}, Loss: {loss.item()}")

#-------------------------------------------------------------------
#4 Пять шагов обучения (The Loop)
optimizer.zero_grad()           # 1. Стираем старые ошибки с доски
pred = model(X)                 # 2. Решаем задачу (Forward)
loss = criterion(pred, y)       # 3. Получаем оценку (Loss)
loss.backward()                # 4. Ищем виноватых (Backprop)
optimizer.step()                # 5. Исправляем веса (Update)

#-------------------------------------------------------------------
#5 Режимы: Учеба vs Экзамен
#Никогда не забывай переключать модель, иначе Dropout испортит предсказания.
#Режим	Код	Что делает
#Учеба	model.train()	Включает Dropout и BatchNorm
#Тест	model.eval()	Выключает "шум", фиксирует веса
#Экономия	with torch.no_grad():	Отключает расчет градиентов (для 4070 это +30% к скорости)

#-------------------------------------------------------------------
#6. Функции потерь (Loss) и Оптимизаторы
#Что выбрать под задачу.
#Классификация: nn.CrossEntropyLoss() (уже содержит Softmax внутри!).
#Регрессия (Числа): nn.MSELoss() (среднеквадратичная ошибка).
#Оптимизатор (Стандарт): torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)
#Weight Decay — это та самая Ridge-регуляризация (L2) от переобучения.

#-------------------------------------------------------------------
#7 Шпаргалка по размерностям (Shape)
#Если код упал с ошибкой RuntimeError: size mismatch:
#Проверь x.shape.
#Первый слой nn.Linear(IN, OUT) должен иметь IN равный количеству признаков в x.
#Используй x.view(-1, size) или nn.Flatten(), чтобы превратить картинку в плоский вектор.

#-------------------------------------------------------------------
#8(Скорость)
# 1. Смешанная точность (Float16) - экономит 2x памяти
scaler = torch.cuda.amp.GradScaler()

# 2. Быстрый перенос данных
train_loader = DataLoader(dataset, batch_size=32, pin_memory=True, num_workers=4)

#--------------------------------------------------------------------------
#9. Прогнозы (Logits)
import torch

# 1. Получаем ответ от модели
outputs = model(x)

# 2. Достаем сами логиты (сырые баллы)
logits = outputs.logits

# 3. Находим класс с максимальным баллом (наш ответ)
# argmax вернет индекс: 0 (негатив) или 1 (позитив)
pred_class = logits.argmax(dim=1)
print(f"Предсказанный класс: {pred_class.item()}")

# 4. Превращаем логиты в понятные человеку проценты (0.0 - 1.0)
pred_prob = torch.softmax(logits, dim=1)
print(f"Вероятности классов: {pred_prob}")

#--------------------------------------------------------------------------
#10. NLP: Текст ⮕ Тензоры (Hugging Face)
from transformers import AutoTokenizer

# 1. Загрузка "мозга" (токенизатора) под конкретную модель
tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny2")

text = "PyTorch на 4070 — это мощно!"

# 2. Превращение в тензоры (Tokenization)
inputs = tokenizer(
    text,
    padding='max_length', # Добить нулями до нужной длины
    truncation=True,      # Обрезать, если текст слишком длинный
    max_length=128,       # Лимит слов (токенов)
    return_tensors="pt"   # Сразу выдать тензоры PyTorch!
)

# Что внутри inputs:
# inputs['input_ids']      — Номера слов в словаре (ID)
# inputs['attention_mask'] — 1 там где текст, 0 там где пустота (Pad)

print(tokenizer.decode(inputs['input_ids'][0]))

#--------------------------------------------------------------------------
#11. NLP: Тренировка (Hugging Face)
import torch
from transformers import AutoModelForSequenceClassification

device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForSequenceClassification.from_pretrained("cointegrated/rubert-tiny2", num_labels=2).to(device)

optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)  # Для BERT LR лучше брать меньше (2e-5)
loss_fn = torch.nn.CrossEntropyLoss()

for epoch in range(10):
    # --- ЭТАП ОБУЧЕНИЯ ---
    model.train()
    for x, y in train_loader:
        x, y = x.to(device), y.to(device)  # Данные на 4070!

        optimizer.zero_grad()
        outputs = model(x)

        logits = outputs.logits  # ДОСТАЕМ ЛОГИТЫ!
        loss = loss_fn(logits, y)

        loss.backward()
        optimizer.step()

    # --- ЭТАП ТЕСТИРОВАНИЯ ---
    model.eval()
    test_loss = 0
    with torch.no_grad():
        for x, y in test_loader:
            x, y = x.to(device), y.to(device)
            outputs = model(x)
            loss = loss_fn(outputs.logits, y)
            test_loss += loss.item()

    print(f"Epoch {epoch}: Train Loss: {loss.item():.4f}, Test Avg Loss: "
          f"{test_loss / len(test_loader):.4f}")

#--------------------------------------------------------------------------
#12. Эмбеддинги: Смысл в числах
import torch
import torch.nn as nn


class EmbeddingModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(num_embeddings=1000, embedding_dim=10)
        self.fc = nn.Linear(10, 2)
        # Softmax УДАЛЯЕМ — CrossEntropy сделает всё сама

    def forward(self, x):
        # x — это ID слов (батч чисел)
        x = self.embedding(x)  # Получаем векторы [batch, seq_len, 10]
        # Для простоты усредняем векторы слов, чтобы получить один вектор на предложение
        x = x.mean(dim=1)
        x = self.fc(x)  # Получаем логиты
        return x


model = EmbeddingModel().to("cuda")  # На твою 4070!
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

for epoch in range(10):
    model.train()  # Устанавливаем режим "Учеба" ПЕРЕД циклом
    for x, y in train_loader:
        x, y = x.to("cuda"), y.to("cuda")  # Данные на карту!

        optimizer.zero_grad()  # 1. Чистим
        pred = model(x)  # 2. Forward
        loss = loss_fn(pred, y)  # 3. Оценка
        loss.backward()  # 4. Градиенты
        optimizer.step()  # 5. Шаг

    print(f"Epoch: {epoch}, Loss: {loss.item()}")
#--------------------------------------------------------------------------
import torch.nn as nn

#13 Слой, который превращает ID (число) в Вектор (смысл)
# 50000 слов в словаре, каждое превращаем в вектор из 768 чисел
embed = nn.Embedding(50000, 768)

# На выходе тензор: [Батч, Длина_текста, 768]
# В этом 768-мерном пространстве "Кот" и "Собака" будут рядом.

#-----------------------------------------------------
#14. Как не "уронить" 4070 (VRAM Management)
#Если видишь ошибку Out of Memory (OOM), делай это по порядку:
#уменьши batch_size (например, с 32 до 16 или 8).
#Уменьши max_length в токенизаторе (со 128 до 64).
#Используй fp16 (Mixed Precision).
#Очисти кэш вручную, если модель упала:
import torch
torch.cuda.empty_cache() # Освободить забитую память GPU



