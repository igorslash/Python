# Начинаем с готового пайплайна для оценки сложности задачи
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
result = classifier("This movie is absolutely fantastic!")
print(result) # [{'label': 'POSITIVE', 'score': 0.9998}]

#обучение своей
# Шаг 1: Выбор и загрузка модели для классификации
from transformers import AutoModelForSequenceClassification
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2) # 2 класса

# Шаг 2: Подготовка данных (датасет с текстами и лейблами)
# ... (здесь код загрузки и токенизации датасета)

# Шаг 3: Запуск обучения
training_args = TrainingArguments(...)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator,
    tokenizer=tokenizer,
)
trainer.train()