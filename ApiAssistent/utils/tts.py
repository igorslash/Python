import pyttsx3

engine = pyttsx3.init()

def text_to_speech(text):
    """Озвучка текста."""
    engine.setProperty('rate', 150)  # Скорость речи
    engine.setProperty('voice', 'ru')  # Язык
    engine.say(text)
    engine.runAndWait()