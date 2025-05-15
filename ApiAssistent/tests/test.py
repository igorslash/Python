from main import listen_for_wake_word
from unittest.mock import patch

@patch("utils.stt_whisper.speech_to_text")
def test_wake_word_detection(mock_stt):
    # Мокаем распознавание речи
    mock_stt.return_value = "привет pyassistant"
    
    # Тест: горячее слово обнаруживается
    assert listen_for_wake_word() == True