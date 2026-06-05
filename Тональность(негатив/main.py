"""
Полный пайплайн: Lightning + BERT + LoRA
Классификация текстов (позитив/негатив) на фейковых данных
"""

import torch
import lightning as pl
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertForSequenceClassification
from peft import get_peft_model, LoraConfig, TaskType

# ──────────────────────────────────────────────
# 1. ДАННЫЕ (фейковые, без внешних файлов)
# ──────────────────────────────────────────────
TRAIN_TEXTS = [
    "отличный продукт советую всем",
    "ужасное качество не покупайте",
    "доставка быстрая упаковка целая",
    "деньги списали товар не прислали",
    "понравился дизайн и материал",
    "полное разочарование потратил время",
    "вежливый персонал помогли выбрать",
    "брак прислали обменять отказались",
] * 16  # множитель чтобы был ненулевой объём

TRAIN_LABELS = [1, 0, 1, 0, 1, 0, 1, 0] * 16  # 1 = позитив, 0 = негатив
VAL_TEXTS = ["хороший сервис приду ещё", "отвратительно не работает"]
VAL_LABELS = [1, 0]

# ──────────────────────────────────────────────
# 2. DATASET (токенизация в __init__)
# ──────────────────────────────────────────────
class TextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=64):
        self.labels = labels
        self.encodings = tokenizer(texts, truncation=True,
                                   padding="max_length",
                                   max_length=max_len,
                                   return_tensors="pt")

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return {
            "input_ids": self.encodings["input_ids"][idx],
            "attention_mask": self.encodings["attention_mask"][idx]
        }, self.labels[idx]

# ──────────────────────────────────────────────
# 3. DATAMODULE
# ──────────────────────────────────────────────
class TextDataModule(pl.LightningDataModule):
    def __init__(self, model_name="bert-base-uncased",
                 batch_size=8, max_len=64):
        super().__init__()
        self.model_name = model_name
        self.batch_size = batch_size
        self.max_len = max_len

    def setup(self, stage=None):
        tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.train_dataset = TextDataset(TRAIN_TEXTS, TRAIN_LABELS,
                                         tokenizer, self.max_len)
        self.val_dataset = TextDataset(VAL_TEXTS, VAL_LABELS,
                                       tokenizer, self.max_len)

    def train_dataloader(self):
        return DataLoader(self.train_dataset,
                          batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self):
        return DataLoader(self.val_dataset,
                          batch_size=self.batch_size)

# ──────────────────────────────────────────────
# 4. LIGHTNING MODULE + LoRA
# ──────────────────────────────────────────────
class BertClassifier(pl.LightningModule):
    def __init__(self, model_name="bert-base-uncased",
                 lr=2e-4, lora_r=8, lora_alpha=16):
        super().__init__()
        # сохраняем гиперпараметры для автоматического логирования
        self.save_hyperparameters()

        # базовая модель
        base_model = BertForSequenceClassification.from_pretrained(
            model_name, num_labels=2)

        # LoRA-адаптер
        lora_config = LoraConfig(
            task_type=TaskType.SEQ_CLS,
            r=self.hparams.lora_r,
            lora_alpha=self.hparams.lora_alpha,
            target_modules=["query", "value"]
        )
        self.model = get_peft_model(base_model, lora_config)
        self.lr = self.hparams.lr

    def forward(self, **inputs):
        return self.model(**inputs)

    def _compute_metrics(self, outputs, labels):
        loss = outputs.loss
        preds = outputs.logits.argmax(dim=1)
        acc = (preds == labels).float().mean()
        return loss, acc

    def training_step(self, batch, batch_idx):
        inputs, labels = batch
        outputs = self(**inputs, labels=labels)
        loss, acc = self._compute_metrics(outputs, labels)
        self.log("train_loss", loss, on_step=True,
                 on_epoch=True, prog_bar=True)
        self.log("train_acc", acc, on_step=True,
                 on_epoch=True, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        inputs, labels = batch
        outputs = self(**inputs, labels=labels)
        loss, acc = self._compute_metrics(outputs, labels)
        self.log("val_loss", loss, on_step=False,
                 on_epoch=True, prog_bar=True)
        self.log("val_acc", acc, on_step=False,
                 on_epoch=True, prog_bar=True)

    def configure_optimizers(self):
        return torch.optim.AdamW(self.parameters(), lr=self.lr)

# ──────────────────────────────────────────────
# 5. ЗАПУСК
# ──────────────────────────────────────────────
def main():
    pl.seed_everything(42)

    dm = TextDataModule(batch_size=4)
    model = BertClassifier(lora_r=8, lora_alpha=16)

    trainer = pl.Trainer(
        max_epochs=3,
        accelerator="auto",
        devices="auto",
        log_every_n_steps=1,
        enable_progress_bar=True,
    )
    trainer.fit(model, dm)

    # финальные метрики
    print("\n--- Итог ---")
    print(f"Trainable params: {
          sum(p.numel() for p in model.parameters() if p.requires_grad):,}")
    print(f"Total params: {
          sum(p.numel() for p in model.parameters()):,}")

if __name__ == "__main__":
    main()