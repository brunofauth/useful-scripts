import pynput.keyboard as pk
import fire
import sys


quit = 0


def on_release(key):
    global quit
    quit = (quit + 1) if (key == pk.Key.esc) else 0
    if quit >= 3:
        return False


def presser(file):
    def on_press(code):
        file.write(str(code).strip("'") + " ")
    return on_press


def main(file: str="pylogtemp.txt"):
    file = file or sys.stdout
    with pk.Listener(on_press=presser(file), on_release=on_release) as l:
        l.join()


if __name__ == "__main__":
    fire.Fire(main)

