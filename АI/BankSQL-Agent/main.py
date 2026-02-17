from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

app = FastAPI()

# Загружаем базовую модель
base_model = "unsloth/Qwen2.5-1.5B-it-bnb-4bit"
adapter_path = "./bank_sql_lora"

tokenizer = AutoTokenizer.from_pretrained(base_model)
model = AutoModelForCausalLM.from_pretrained(base_model, torch_dtype=torch.float16, device_map="auto")
model = PeftModel.from_pretrained(model, adapter_path)

@app.get("/generate")
def generate(prompt: str):
    full_prompt = f"### Instruction:\n{prompt}\n\n### Response:\n"
    inputs = tokenizer(full_prompt, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=64)
    return {"sql": tokenizer.decode(outputs[0], skip_special_tokens=True).split("### Response:\n")[-1]}
