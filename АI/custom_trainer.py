from transformers import AutoTokenizer, AutoModelForSequenceClassification, DataCollatorWithPadding, get_scheduler
from datasets import load_dataset
from torch.utils.data import DataLoader
import torch
from tqdm.auto import tqdm

# 1. Загрузка и подготовка данных
dataset = load_dataset("imdb")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = (AutoModelForSequenceClassification
         .from_pretrained("bert-base-uncased", num_labels=2))


def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True)


tokenized_datasets = dataset.map(preprocess_function, batched=True)
tokenized_datasets = tokenized_datasets.rename_column("label", "labels")
tokenized_datasets.set_format("torch")

# 2. Создание DataLoader и data collator
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
train_loader = DataLoader(tokenized_datasets["train"], shuffle=True, batch_size=16, collate_fn=data_collator)
eval_loader = DataLoader(tokenized_datasets["test"], batch_size=16, collate_fn=data_collator)

# 3. Настройка обучения
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

num_epochs = 3
num_training_steps = num_epochs * len(train_loader)
lr_scheduler = get_scheduler("linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=num_training_steps)

# 4. Цикл обучения
progress_bar = tqdm(range(num_training_steps))
model.train()

for epoch in range(num_epochs):
    for batch in train_loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        loss = outputs.loss

        loss.backward()
        optimizer.step()
        lr_scheduler.step()
        optimizer.zero_grad()
        progress_bar.update(1)

        progress_bar.set_description(f"Epoch {epoch + 1}, "
                                     f"Loss: {loss.item():.4f}")

# 5. Оценка модели
model.eval()
total_correct = 0
total_samples = 0

for batch in eval_loader:
    batch = {k: v.to(device) for k, v in batch.items()}
    with torch.no_grad():
        outputs = model(**batch)

    predictions = torch.argmax(outputs.logits, dim=-1)
    total_correct += (predictions == batch["labels"]).sum().item()
    total_samples += len(batch["labels"])

accuracy = total_correct / total_samples
print(f"Validation Accuracy: {accuracy:.4f}")

# 6. Сохранение модели
model.save_pretrained("./fine-tuned-bert-model")
tokenizer.save_pretrained("./fine-tuned-bert-model")