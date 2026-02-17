# Шаг 1: Загрузка модели, предназначенной для MLM
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForMaskedLM.from_pretrained(model_name)

# Шаг 2: Подготовка данных (просто тексты, без разметки)
# ... (здесь код загрузки и токенизации датасета)

# Шаг 3: Запуск обучения с специальным DataCollator для MLM
from transformers import DataCollatorForLanguageModeling
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=0.15)

training_args = TrainingArguments(...)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator, # ✅ Ключевой момент!
    tokenizer=tokenizer,
)
trainer.train()