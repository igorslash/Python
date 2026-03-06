# Базовый образ с Python и CUDA (если есть GPU)
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем папку для логов
RUN mkdir -p logs

# Команда по умолчанию
CMD ["python", "main.py"]