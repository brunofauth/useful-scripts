from win32com.client import Dispatch
from fire import Fire

def speak(text):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

if __name__ == "__main__":
    Fire(speak)