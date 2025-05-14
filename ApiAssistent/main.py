from utils.audio_utils import record_audio
from utils.stt_whisper import speech_to_text
from utils.gpt_client import ask_gpt
from utils.tts import text_to_speech

def listen_for_wake_word():
    """Wait word"""
    print("🔍 Listen 'Hello, Assistant...")
    while True:
        audio_data = record_audio()
        text = speech_to_text(audio_data)
        if text == "Hello, Assistant":
            print("✅ Wake word detected")
            return True
def main():
    print("🟢 PyAssistant запущен!")
    while True:
        if listen_for_wake_word():
            text_to_speech("Чем могу помочь?")
            audio = record_audio(duration=7)
            user_text = speech_to_text(audio)
            print(f"Вы: {user_text}")

            if "стоп" in user_text.lower():
                text_to_speech("До свидания!")
                break

            response = ask_gpt(user_text)
            print(f"AI: {response}")
            text_to_speech(response)

if __name__ == "__main__":
    main()