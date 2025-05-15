from utils.gpt_client import ask_gpt

def test_ask_gpt(monkeypatch):
    # Заменяем реальный запрос на заглушку
    def mock_gpt_response(*args, **kwargs):
        return "Это тестовый ответ."
    
    monkeypatch.setattr("openai.ChatCompletion.create", mock_gpt_response)
    
    # Тест: GPT возвращает непустую строку
    response = ask_gpt("Как дела?")
    assert isinstance(response, str)
    assert len(response) > 0