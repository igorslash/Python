import numpy as np
from utils.audio_utils import record_audio

def test_record_audio():
    # Тест: запись аудио возвращает numpy-массив
    audio = record_audio(duration=1)  # Запись 1 секунды
    assert isinstance(audio, np.ndarray)
    assert len(audio) > 0