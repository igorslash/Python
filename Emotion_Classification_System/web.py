from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer

app = FastAPI()  # Создаем сервер

# Загружаем модель (в реальности лучше грузить из чекпоинта)
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = ProEmotionClassifier.load_from_checkpoint("emotion_model.ckpt")
model.eval()  # Переводим в режим предсказания


class TextRequest(BaseModel):
    text: str


@app.post("/predict")
async def predict_emotion(request: TextRequest):
    # Токенизируем входящий текст
    inputs = tokenizer(request.text, return_tensors="pt", truncation=True, max_length=128)

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        prediction = torch.argmax(probs, dim=1).item()

    label = "Positive" if prediction == 1 else "Negative"
    confidence = probs[0][prediction].item()

    return {"text": request.text, "emotion": label, "confidence": f"{confidence:.2%}"}
