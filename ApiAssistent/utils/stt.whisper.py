import whisper
from config import WHISPER_MODEL

model = whisper.load_model(WHISPER_MODEL)

def speech_to_text(audio_data, sample_rate = 16000):
    """Translate Audio Text"""
    audio = whisper.pad_or_trim(audio_data)
    result = model.transcribe(audio, fp16=False, language='ru')
    return result['text']