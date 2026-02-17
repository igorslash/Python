import torch
from unsloth import FastLanguageModel
from datasets import Dataset
import pandas as pd
import json

# 2. Загрузка модели (без изменений)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Qwen2.5-1.5B-it-bnb-4bit",
    max_seq_length = 2048,
    load_in_4bit = True,
)

# 3. Настройка LoRA (без изменений)
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",
)

# 4. ПОДГОТОВКА ДАННЫХ
file_path = "/Users/admin/PycharmProjects/АI/BankSQL-Agent/schema.sql"

data_list = []
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data_list.append(json.loads(line))
        except:
            continue # Пропускаем битые строки

# Превращаем в датасет Hugging Face напрямую, минуя мучения с Pandas
dataset = Dataset.from_list(data_list)

# Шаблон промпта (добавили контекст, чтобы модель знала схему БД)
def format_prompts(examples):
    instructions = examples["instruction"]
    outputs      = examples["output"]
    texts = []
    for instruction, output in zip(instructions, outputs):
        text = f"### System:\nТы банковский SQL-ассистент. Пиши только SQL-код.\n\n### Instruction:\n{instruction}\n\n### Response:\n{output}"
        texts.append(text)
    return { "text" : texts, }

dataset = dataset.map(format_prompts, batched = True)

# 5. Запуск обучения (SFTTrainer)
from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model = model,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = 2048,
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        max_steps = 60, # 60 шагов на 50 строк - это примерно 5-10 эпох. Идеально.
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        output_dir = "outputs",
    ),
)

trainer.train()
