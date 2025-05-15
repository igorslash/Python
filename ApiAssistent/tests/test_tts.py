from utils.tts import text_to_speech

def test_text_to_speech(capsys):
    # Тест: функция выполняется без ошибок
    text_to_speech("Тестовый текст")
    captured = capsys.readouterr()
    assert "Ошибка" not in captured.out  # Проверяем, что нет ошибок