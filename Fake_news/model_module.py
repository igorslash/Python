import lightning as L
import torch
import torchmetrics
from transformers import AutoModelForSequenceClassification

class FakeNewsModel(L.LightningModule):
    def __init__(self, model_name, lr=2e-5):
        super().__init__()
        self.save_hyperparameters()
        
        # Модель
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name, 
            num_labels=2  # бинарная классификация
        )
        
        # Метрики
        self.train_accuracy = torchmetrics.Accuracy(task="binary")
        self.val_accuracy = torchmetrics.Accuracy(task="binary")
        self.val_f1 = torchmetrics.F1Score(task="binary")
        self.test_accuracy = torchmetrics.Accuracy(task="binary")
        self.test_f1 = torchmetrics.F1Score(task="binary")
        
    def forward(self, batch):
        return self.model(**batch)
    
    def training_step(self, batch, batch_idx):
        outputs = self(batch)
        loss = outputs.loss
        
        # Логируем loss
        self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True)
        
        # Считаем accuracy на train
        preds = torch.argmax(outputs.logits, dim=1)
        self.train_accuracy(preds, batch["labels"])
        self.log("train_acc", self.train_accuracy, on_step=False, on_epoch=True)
        
        return loss

    def validation_step(self, batch, batch_idx):
        outputs = self(batch)
        loss = outputs.loss
        preds = torch.argmax(outputs.logits, dim=1)
        
        # Логируем валидационные метрики
        self.log("val_loss", loss, on_epoch=True, prog_bar=True)
        self.val_accuracy(preds, batch["labels"])
        self.val_f1(preds, batch["labels"])
        self.log("val_acc", self.val_accuracy, on_epoch=True, prog_bar=True)
        self.log("val_f1", self.val_f1, on_epoch=True, prog_bar=True)
        
    def test_step(self, batch, batch_idx):
        outputs = self(batch)
        preds = torch.argmax(outputs.logits, dim=1)
        
        self.test_accuracy(preds, batch["labels"])
        self.test_f1(preds, batch["labels"])
        self.log("test_acc", self.test_accuracy, on_epoch=True)
        self.log("test_f1", self.test_f1, on_epoch=True)
        
    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.parameters(), lr=self.hparams.lr)
        
        # Добавляем scheduler для плавного снижения learning rate
        scheduler = torch.optim.lr_scheduler.LinearLR(
            optimizer, 
            start_factor=1.0,
            end_factor=0.1,
            total_iters=3  # за 3 эпохи
        )
        
        return {
            "optimizer": optimizer,
            "lr_scheduler": {
                "scheduler": scheduler,
                "interval": "epoch"
            }
        }
