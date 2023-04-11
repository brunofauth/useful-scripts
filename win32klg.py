import contextlib
import ctypes.wintypes
import ctypes_helper
import winfunc


WH_KEYBOARD_LL = 0xD
WM_KEYDOWN = 0x0100


@contextlib.contextmanager
def windows_hook(type, func):
    hook = None
    try:
        hook = winfunc.set_hook(type, func, winfunc.get_module_handle(None), 0)
        yield hook
    finally:
        winfunc.del_hook(hook)


# https://msdn.microsoft.com/pt-br/library/windows/desktop/ms644985(v=vs.85).aspx
@winfunc.HOOKPROC
def print_kb_events(nCode, wParam, lParam):
    print(nCode, wParam, ctypes_helper.KBDLLHOOKSTRUCT.from_address(lParam))
    # with open("My-Awesome-file.txt", "a") as file:
        # print(nCode, wParam, lParam[0], lParam[1], lParam[2], lParam[3], lParam[4], file=file)
        # print(nCode, wParam, lParam, file=file)
    
    return winfunc.next_hook(None, nCode, wParam, lParam)


with windows_hook(WH_KEYBOARD_LL, print_kb_events):
    msg, code = winfunc.get_message(None, 0, 0)
    print(msg, code)
