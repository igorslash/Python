import torch
import pytorch_lightning as pl
from torchmetrics import Accuracy, F1Score
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class ProEmotionClassifier(pl.LightningModule):
    def __init__(self, model_name="distilbert-base-uncased"):
        super().__init__()
        self.save_hyperparameters()  # Сохраняет конфиг модели автоматически
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

        # Метрики (из библиотеки torchmetrics)
        self.train_acc = Accuracy(task="multiclass", num_classes=2)
        self.val_acc = Accuracy(task="multiclass", num_classes=2)
        self.val_f1 = F1Score(task="multiclass", num_classes=2)

    def forward(self, input_ids, attention_mask, labels=None):
        return self.model(input_ids, attention_mask=attention_mask, labels=labels)

    def training_step(self, batch):
        outputs = self(**batch)
        loss = outputs.loss
        preds = torch.argmax(outputs.logits, dim=1)

        # Логируем лосс и точность на обучении
        self.train_acc(preds, batch["labels"])
        self.log("train_loss", loss, prog_bar=True)
        self.log("train_acc", self.train_acc, prog_bar=True)
        return loss

    def validation_step(self, batch):
        outputs = self(**batch)
        val_loss = outputs.loss
        preds = torch.argmax(outputs.logits, dim=1)

        # Считаем метрики на валидации (самое важное для резюме)
        self.val_acc(preds, batch["labels"])
        self.val_f1(preds, batch["labels"])

        self.log("val_loss", val_loss, prog_bar=True)
        self.log("val_acc", self.val_acc, prog_bar=True)
        self.log("val_f1", self.val_f1, prog_bar=True)

    def configure_optimizers(self):
        return torch.optim.AdamW(self.parameters(), lr=2e-5)

# После обучения сохраняем веса:
trainer.save_checkpoint("emotion_model.ckpt")
