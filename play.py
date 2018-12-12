# coding: UTF-8

import time
import fire
import os

def play(name):
    now = str(time.time())
    try:
        os.system(f"youtube-dl --default-search auto -o {now}.%(EXT)s \"{name}\"") # se der probs aq fudeu
        filename = tuple(filter(lambda x: x.startswith(now), os.listdir()))[0]
        os.system(fr'"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe" -I dummy --dummy-quiet --play-and-exit {filename}')
    finally:
        os.remove(filename)

if __name__ == "__main__":
    fire.Fire(play)
