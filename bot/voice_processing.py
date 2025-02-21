import speech_recognition as sr
import soundfile as sf
from gtts import gTTS
import os


def voice_to_text(message_id, ogg_file):
    """Преобразование голоса в текст"""
    # Конвертация OGG в WAV
    wav_file = f"{message_id}_voice.wav"
    data, samplerate = sf.read(ogg_file)
    sf.write(wav_file, data, samplerate)

    # Преобразование голоса в текст
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ru-RU")
            print(f"Распознанный текст: {text}")
            # bot.reply_to(message, f"Распознанный текст: {text}")
        except sr.UnknownValueError:
            text = "Не удалось распознать речь."
        except sr.RequestError as e:
            text = f"Ошибка распознавания: {e}"
    # Удаление временных файлов
    os.remove(ogg_file)
    os.remove(wav_file)

    return text


def text_to_voice(message_id, text):
    """Преобразование текста в голос"""
    tts = gTTS(text=text, lang="ru")
    output_voice_file = f"{message_id}_response.mp3"
    tts.save(output_voice_file)

    return output_voice_file
