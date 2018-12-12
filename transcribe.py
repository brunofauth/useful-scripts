import speech_recognition as sr
import fire
import time
import os

DL_CMD = 'youtube-dl --no-playlist --geo-bypass --output "{name}.%(ext)s" --audio-format wav --format bestaudio --extract-audio {url}'

def transcribe(url):
    timestamp = time.time()
    recognizer = sr.Recognizer()
    os.system(DL_CMD.format(name=timestamp, url=url))
    with sr.AudioFile(f"{timestamp}.wav") as file:
        audio = recognizer.record(file)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError, sr.RequestError:
        return None

if __name__ == "__main__":
    fire.Fire(transcribe)