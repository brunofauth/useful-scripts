import ctypes.wintypes
import ctypes


if ctypes.sizeof(ctypes.c_void_p) == 8:
    ctypes.wintypes.ULONG_PTR = ctypes.c_ulonglong
    ctypes.wintypes.LONG_PTR = ctypes.c_longlong
else:
    ctypes.wintypes.ULONG_PTR = ctypes.c_ulong
    ctypes.wintypes.LONG_PTR = ctypes.c_long
ctypes.wintypes.LRESULT = ctypes.wintypes.LONG_PTR
ctypes.wintypes.LPCTSTR = ctypes.wintypes.LPCWSTR
ctypes.wintypes.LPDWORD = ctypes.wintypes.PDWORD 
ctypes.wintypes.SIZE_T = ctypes.wintypes.ULONG_PTR



def _repr_fields(obj):
    fields = {name: getattr(obj, name) for name, type in obj.__class__._fields_}
    return f"{obj.__class__.__name__}({fields})"


def struct(cls):
    attrs = {**vars(cls), "_fields_": tuple(cls.__annotations__.items())}
    attrs["__repr__"] = _repr_fields
    return type(cls.__name__, (ctypes.Structure, *cls.__bases__), attrs)


def union(cls):
    attrs = {**vars(cls), "_fields_": tuple(cls.__annotations__.items())}
    attrs["__repr__"] = _repr_fields
    return type(cls.__name__, (ctypes.Union, *cls.__bases__), attrs)


@struct
class KBDLLHOOKSTRUCT:
    vkCode:      ctypes.wintypes.DWORD
    scanCode:    ctypes.wintypes.DWORD
    flags:       ctypes.wintypes.DWORD
    time:        ctypes.wintypes.DWORD
    dwExtraInfo: ctypes.wintypes.ULONG_PTR


@struct
class MSLLHOOKSTRUCT:
    pt: ctypes.wintypes.POINT
    mouseData: ctypes.wintypes.DWORD
    flags: ctypes.wintypes.DWORD
    time: ctypes.wintypes.DWORD
    dwExtraInfo: ctypes.wintypes.ULONG_PTR


@struct
class MOUSEINPUT:
    dx: ctypes.wintypes.LONG
    dy: ctypes.wintypes.LONG
    mouseData: ctypes.wintypes.DWORD
    dwFlags: ctypes.wintypes.DWORD
    time: ctypes.wintypes.DWORD
    dwExtraInfo: ctypes.wintypes.ULONG_PTR


@struct
class KEYBDINPUT:
    wVk: ctypes.wintypes.WORD
    wScan: ctypes.wintypes.WORD
    dwFlags: ctypes.wintypes.DWORD
    time: ctypes.wintypes.DWORD
    dwExtraInfo: ctypes.wintypes.ULONG_PTR


@struct
class HARDWAREINPUT:
    uMsg: ctypes.wintypes.DWORD
    wParamL: ctypes.wintypes.WORD
    wParamH: ctypes.wintypes.WORD


@struct
class INPUT:
    @union
    class _INPUT:
        ki: KEYBDINPUT
        mi: MOUSEINPUT
        hi: HARDWAREINPUT
    _anonymous_ = ("_input",)
    type: ctypes.wintypes.DWORD
    _input: _INPUT


ctypes.wintypes.LPINPUT = ctypes.POINTER(INPUT)


@struct
class MODULEINFO:
    lpBaseOfDll: ctypes.wintypes.LPVOID
    SizeOfImage: ctypes.wintypes.DWORD
    EntryPoint:  ctypes.wintypes.LPVOID