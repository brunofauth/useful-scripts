import fire
import sys
import os


def speak(text):
    if sys.platform == "win32":
        import win32com.client
        win32com.client.Dispatch("SAPI.SpVoice").speak(text)
    else:
        os.system("espeak '{text}'")


if __name__ == "__main__":
    fire.Fire(speak)
