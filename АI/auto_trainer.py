from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding
from datasets import load_dataset

# 1. Загрузка данных
dataset = load_dataset("imdb")

# 2. Загрузка модели и токенизатора
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

# 3. Токенизация данных
def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True)

tokenized_datasets = dataset.map(preprocess_function, batched=True)
tokenized_datasets = tokenized_datasets.rename_column("label", "labels")
tokenized_datasets.set_format("torch")

# 4. Настройка обучения
training_args = TrainingArguments(
    output_dir="./fine-tuned-bert-model",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    save_strategy="epoch",
    load_best_model_at_end=True,
)

# 5. Создание data collator
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# 6. Запуск обучения (ВСЁ АВТОМАТИЧЕСКИ)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],  # В IMDB test = validation
    tokenizer=tokenizer,
    data_collator=data_collator,
)

trainer.train()
trainer.evaluate()

# Модель автоматически сохраняется в output_dir