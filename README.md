# Fake News Detection with PyTorch Lightning

Проект по классификации новостей на достоверные и фейковые с использованием **BERT** и **PyTorch Lightning**.

## 📊 Датасет
- 4000+ новостных статей
- Бинарная классификация (fake/real)
- Очистка: удаление пустых и коротких текстов

## 🏗 Архитектура
- Модель: `bert-base-uncased` с fine-tuning
- Фреймворк: PyTorch Lightning
- Метрики: Accuracy, F1-score
- Оптимизация: Mixed precision (16-bit), Early stopping

## 📈 Результаты
- Accuracy на валидации: **0.92**
- F1-score на валидации: **0.89**
- Сохраняется лучшая модель по F1

## 🚀 Запуск
```bash
pip install -r requirements.txt
python main.py

