import lightning as L
from torch.utils.data import DataLoader
from datasets import load_dataset
from transformers import AutoTokenizer, DataCollatorWithPadding

class FakeNewsDataModule(L.LightningDataModule):
    def __init__(self, model_name, file_path, batch_size=16):
        super().__init__()
        self.model_name = model_name
        self.file_path = file_path
        self.batch_size = batch_size
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.collator = DataCollatorWithPadding(self.tokenizer)

    def setup(self, stage=None):
        # Загружаем датасет
        ds = load_dataset("csv", data_files=self.file_path)["train"]
        
        # Чистка данных (убираем пустые и короткие тексты)
        def clean_text(example):
            # Проверяем, что текст есть и это строка
            if not example.get("text") or not isinstance(example["text"], str):
                return False
            # Убираем слишком короткие тексты (меньше 5 слов)
            if len(example["text"].split()) < 5:
                return False
            return True
        
        ds = ds.filter(clean_text)
        
        # Токенизация
        def tokenize(batch):
            return self.tokenizer(
                batch["text"], 
                truncation=True, 
                max_length=512,
                padding=False  # collator сделает padding позже
            )
        
        # Добавляем метки (labels), предполагаем, что в датасете есть колонка 'label'
        tokenized = ds.map(tokenize, batched=True)
        
        # Разделяем на train/val/test (70/15/15)
        train_val = tokenized.train_test_split(test_size=0.3, seed=42)
        val_test = train_val["test"].train_test_split(test_size=0.5, seed=42)
        
        self.train_ds = train_val["train"]
        self.val_ds = val_test["train"]
        self.test_ds = val_test["test"]
        
        print(f"Train: {len(self.train_ds)}, Val: {len(self.val_ds)}, Test: {len(self.test_ds)}")

    def train_dataloader(self):
        return DataLoader(
            self.train_ds, 
            batch_size=self.batch_size, 
            collate_fn=self.collator,
            shuffle=True
        )

    def val_dataloader(self):
        return DataLoader(
            self.val_ds, 
            batch_size=self.batch_size, 
            collate_fn=self.collator
        )

    def test_dataloader(self):
        return DataLoader(
            self.test_ds, 
            batch_size=self.batch_size, 
            collate_fn=self.collator
        )