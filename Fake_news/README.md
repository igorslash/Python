## 🐳 Запуск в Docker

### Требования
- Docker 20.10+
- Docker Compose 2.0+
- NVIDIA Container Toolkit (для GPU)

### Быстрый старт

```bash
# 1. Собрать образ
make build

# 2. Запустить обучение
make run

# 3. В отдельном терминале запустить TensorBoard
make tensorboard
# Открой http://localhost:6006

# 4. Остановить
make stop