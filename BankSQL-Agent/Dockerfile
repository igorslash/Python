# 1. Базовый образ с поддержкой CUDA (для скорости)
FROM nvidia/cuda:12.1.0-base-ubuntu22.04

# 2. Ставим Python
RUN apt-get update && apt-get install -y python3 python3-pip

# 3. Рабочая директория
WORKDIR /app

# 4. Копируем зависимости и ставим их
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 5. Копируем код и веса твоей модели (папку с LoRA)
COPY main.py .
COPY bank_sql_lora/ ./bank_sql_lora/

# 6. Запускаем сервер
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
