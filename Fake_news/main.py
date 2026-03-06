import lightning as L
from lightning.pytorch.callbacks import EarlyStopping, ModelCheckpoint
from lightning.pytorch.loggers import TensorBoardLogger

# Импортируем наши модули
from data_module import FakeNewsDataModule
from model_module import FakeNewsModel

# 1. Data Module
dm = FakeNewsDataModule(
    model_name="bert-base-uncased", 
    file_path="C:\Users\User\PycharmProjects\Training\АI\Fake_news\fake_news_dataset_4000_rows.csv",  # укажи свой путь
    batch_size=16
)

# 2. Model
model = FakeNewsModel(model_name="bert-base-uncased", lr=2e-5)

# 3. Callbacks
early_stop = EarlyStopping(
    monitor="val_f1",  # следим за F1
    mode="max",        # хотим максимизировать
    patience=2,        # ждём 2 эпохи без улучшений
    verbose=True
)

checkpoint = ModelCheckpoint(
    monitor="val_f1",
    mode="max",
    filename="best-model-{epoch:02d}-{val_f1:.3f}",
    save_top_k=1,
    verbose=True
)

# 4. Logger (чтобы смотреть графики в TensorBoard)
logger = TensorBoardLogger("logs/", name="fakenews")

# 5. Trainer
trainer = L.Trainer(
    max_epochs=5,
    accelerator="auto",
    devices=1,
    precision="16-mixed",  # экономит память
    callbacks=[early_stop, checkpoint],
    logger=logger,
    log_every_n_steps=10
)

# 6. Обучение
trainer.fit(model, datamodule=dm)

# 7. Тестирование (после обучения)
trainer.test(model, datamodule=dm)

print(f"Лучшая модель сохранена: {checkpoint.best_model_path}")
print(f"Лучший F1 на валидации: {checkpoint.best_model_score:.4f}")
