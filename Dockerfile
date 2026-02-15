# 1. Берем базовый образ с Python и PyTorch
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# 2. Указываем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Копируем список библиотек и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем весь наш код и веса модели в контейнер
COPY . .

# 5. Открываем порт 8000 для нашего API на FastAPI
EXPOSE 8000

# 6. Команда для запуска сервера при старте контейнера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
