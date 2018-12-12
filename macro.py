#! /usr/bin/env python
# coding: UTF-8

# Works but execution takes too long.


import pynput.keyboard as pk
import pynput.mouse as pm
import dataclasses
import threading
import functools
import inspect
import struct
import types
import time
import fire


@dataclasses.dataclass
class Input:
    type: int
    x: int = 0
    y: int = 0
    dx: int = 0
    dy: int = 0
    button: int = 255
    pressed: bool = 0
    key: int = 0
    time: float = 0


__all__ = ["record_macro", "play_macro"]
InputStruct = struct.Struct("BIIIIB?Hf") # 29 bytes
INPUT_TYPE = ["position", "click", "scroll", "press", "release"]


def lock_method(lock, method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        with lock:
            return method(*args, **kwargs)
    return wrapper


class SimpleQueue(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        lock = threading.Lock()
        for name, func in inspect.getmembers(self, inspect.ismethoddescriptor):
            setattr(self, name, lock_method(lock, func))


class RecHandler(object):
    def __init__(self, exit_key=pk.Key.f8):
        self.eventq = SimpleQueue()
        self.exit_key = exit_key

    def position(self, x, y):
        self.eventq.append(Input(type=0, x=x, y=y, time=time.time()))

    def click(self, x, y, button, pressed):
        self.eventq.append(Input(type=1, x=x, y=y, button=button.name, pressed=pressed, time=time.time()))

    def scroll(self, x, y, dx, dy):
        self.eventq.append(Input(type=2, x=x, y=y, dx=dx, dy=dy, time=time.time()))

    def press(self, key):
        if key == self.exit_key:
            return False
        self.eventq.append(Input(type=3, key=key.value.vk, time=time.time()))

    def release(self, key):
        self.eventq.append(Input(type=4, key=key.value.vk, time=time.time()))


class RunHandler(object):
    def __init__(self):
        # Perhaps multiple inheritance is more elegant
        self.kc = pk.Controller()
        self.mc = pm.Controller()
    
    def position(self, e):
        self.mc.position = e.x, e.y

    def click(self, e):
        button = getattr(pm.Button, e.button)
        self.mc.press(button) if e.pressed else self.mc.release(button)

    def scroll(self, e):
        self.mc.scroll(e.dx, e.dy)

    def press(self, e):
        self.kc.release(pk.KeyCode.from_vk(e.key))

    def release(self, e):
        self.kc.release(pk.KeyCode.from_vk(e.key))


def record_macro(filepath: str, delay=3, save_origin=False) -> None:
    print("Loading...")
    time.sleep(delay)
    start = time.time()
    h = RecHandler()
    
    print("Recording...")
    kl = pk.Listener(on_press=h.press, on_release=h.release)
    ml = pm.Listener(on_move=h.position, on_click=h.click, on_scroll=h.scroll)
    with kl, ml:
        kl.join()
    
    end = time.time()
    print("Saving...")
    # adjust "time"s to use variations instead of absolutes
    for i in range(len(h.eventq) - 1, 0, -1):
        h.eventq[i].time -= h.eventq[i - 1].time
    h.eventq[0].time -= start
    
    with open(filepath, "wb") as file:
        for event in h.eventq:
            file.write(InputStruct.pack(*dataclasses.astuple(event)))
    
    for event in h.eventq:
        print(INPUT_TYPE[event.type], event.x, event.y, event.time)
    
    print(f"Done! This macro lasts {sum(e.time for e in h.eventq)} instead of {time.time() - start} seconds.")


def play_macro(filepath: str, delay=3, afap=False, speed=1) -> None:
    print("Loading...")
    time.sleep(delay)
    handler = RunHandler()
    with open(filepath, "rb") as file:
        events = file.read()
    
    start = time.time()
    print("Playing...")
    for event in (Input(*x) for x in InputStruct.iter_unpack(events)):
        if not afap:
            time.sleep(event.time / speed)
        getattr(handler, INPUT_TYPE[event.type])(event)
    
    print(f"Done! This macro lasted {time.time() - start} seconds.")


if __name__ == "__main__":
    fire.Fire({"rec": record_macro, "play": play_macro})
