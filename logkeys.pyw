from pynput.keyboard import Listener, Key
from fire import Fire
from sys import stdout

quit = 0

def on_release(key):
    global quit
    quit = (quit + 1) if (key == Key.esc) else 0
    if quit >= 3:
        return False

def presser(file):
    def on_press(code):
        file.write(str(code).strip("'") + " ")
    return on_press

def main(file: str="pylogtemp.txt"):
    if not file:
        with Listener(on_press=presser(stdout), on_release=on_release) as l:
            l.join()
    else:
        with open(file, "w") as output:
            l = Listener(on_press=presser(output), on_release=on_release)
            with l:
                l.join()

if __name__ == "__main__":
    Fire(main)