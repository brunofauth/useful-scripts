from fire import Fire

import pygame
import os

def play_folder(folder):
    has_loaded_first_bc_of_buggy_api = False
    for file in os.listdir(folder):
        try:
            if not has_loaded_first_bc_of_buggy_api:
                pygame.mixer.music.load(os.path.join(folder, file))
                has_loaded_first_bc_of_buggy_api = True
            else:
                pygame.mixer.music.queue(os.path.join(folder, file))
        except pygame.error:
            pass
    pygame.mixer.music.play()

if __name__ == "__main__":
    pygame.mixer.init()
    Fire(play_folder)