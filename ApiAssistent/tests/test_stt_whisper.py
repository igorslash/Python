import numpy as np
from utils.stt_whisper import speech_to_text

def test_speech_to_text():
    # Создаем "заглушку" аудио (тишина)
    dummy_audio = np.zeros(16000, dtype=np.float32)  # 1 сек тишины (16 kHz)
    
    # Тест: Whisper возвращает строку (даже пустую)
    text = speech_to_text(dummy_audio)
    assert isinstance(text, str)