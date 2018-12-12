import ctypes.wintypes
import ctypes
import ctypes_helper


def errcheck(checker):
    def wrapped(result, func, args):
        print("result =", result)
        if checker(result):
            raise ctypes.WinError(ctypes.get_last_error())
        return result
    return wrapped


HOOKPROC = ctypes.WINFUNCTYPE(
    ctypes.wintypes.LRESULT,
    ctypes.c_int32,
    ctypes.wintypes.WPARAM,
    ctypes.wintypes.LPARAM)


# https://msdn.microsoft.com/pt-br/library/windows/desktop/ms644990(v=vs.85).aspx
_SetWindowsHookExW = ctypes.windll.user32.SetWindowsHookExW
_SetWindowsHookExW.restype = ctypes.wintypes.HHOOK
_SetWindowsHookExW.errcheck = errcheck(lambda x: x is None)
_SetWindowsHookExW.argtypes = [
    ctypes.c_int,              # idHook
    HOOKPROC,                  # lpfn
    ctypes.wintypes.HINSTANCE, # hMod
    ctypes.wintypes.DWORD]     # dwThreadId


def set_hook(hook_id, func, module, thread_id):
    return _SetWindowsHookExW(hook_id, func, module, thread_id)


_CallNextHookEx = ctypes.windll.user32.CallNextHookEx
_CallNextHookEx.restype = ctypes.wintypes.LRESULT
_CallNextHookEx.errcheck = errcheck(lambda x: False)
_CallNextHookEx.argtypes = [
    ctypes.wintypes.HHOOK,  # hhk
    ctypes.c_int,           # nCode
    ctypes.wintypes.WPARAM, # wParam
    ctypes.wintypes.LPARAM]


def next_hook(hook, n_code, w_param, l_param):
    return _CallNextHookEx(hook, n_code, w_param, l_param)


_UnhookWindowsHookEx = ctypes.windll.user32.UnhookWindowsHookEx
_UnhookWindowsHookEx.restype = ctypes.wintypes.BOOL
# _UnhookWindowsHookEx.errcheck = errcheck(lambda x: x == 0)
_UnhookWindowsHookEx.argtypes = [ctypes.wintypes.HHOOK]


def del_hook(hook):
    return _UnhookWindowsHookEx(hook)


# https://msdn.microsoft.com/pt-br/library/windows/desktop/ms644936(v=vs.85).aspx
_GetMessageW = ctypes.windll.user32.GetMessageW
_GetMessageW.restype = ctypes.wintypes.BOOL
_GetMessageW.errcheck = errcheck(lambda x: x == -1)
_GetMessageW.argtypes = (
    ctypes.wintypes.LPMSG,
    ctypes.wintypes.HWND,
    ctypes.wintypes.UINT,
    ctypes.wintypes.UINT)


def get_message(window, min_msg, max_msg):
    msg = ctypes.wintypes.MSG()
    ret = _GetMessageW(msg, window, min_msg, max_msg)
    return ret, msg


# https://msdn.microsoft.com/pt-br/library/windows/desktop/ms683199(v=vs.85).aspx
_GetModuleHandleW = ctypes.windll.kernel32.GetModuleHandleW
_GetModuleHandleW.restype = ctypes.wintypes.HMODULE
_GetModuleHandleW.errcheck = errcheck(lambda x: x is None)
_GetModuleHandleW.argtypes = [ctypes.wintypes.LPCTSTR]


def get_module_handle(module_name):
    return _GetModuleHandleW(module_name)


_SendInput = ctypes.windll.user32.SendInput
_SendInput.restype = ctypes.wintypes.UINT
_SendInput.errcheck = errcheck(lambda x: False)
_SendInput.argtypes = [
    ctypes.wintypes.UINT,   # nInputs
    ctypes.wintypes.LPINPUT,# pInputs
    ctypes.c_int]           # cbSize


def send_input(inputs_array):
    _SendInput(len(inputs_array), ctypes.addressof(a), ctypes.sizeof(ctypes_helper.INPUT))


#_OpenProcess = win32api.OpenProcess
_OpenProcess = ctypes.windll.kernel32.OpenProcess
_OpenProcess.restype = ctypes.wintypes.HANDLE
_OpenProcess.errcheck = errcheck(lambda result: result is None)
_OpenProcess.argtypes = [
    ctypes.wintypes.DWORD,  # dwFlags
    ctypes.wintypes.BOOL,   # bInheritHandle
    ctypes.wintypes.DWORD]  # dwProcessId


def open_process(id, flags=0, inherit=False):
    return _OpenProcess(flags, inherit, id)


#_CloseHandle = win32api.CloseHandle
_CloseHandle = ctypes.windll.kernel32.CloseHandle
_CloseHandle.restype = ctypes.wintypes.BOOL
_CloseHandle.errcheck = errcheck(lambda result: result == 0)
_CloseHandle.argtypes = [ctypes.wintypes.HANDLE]


def close_handle(handle):
    return _CloseHandle(handle)
    

_ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
_ReadProcessMemory.restype = ctypes.wintypes.BOOL
_ReadProcessMemory.errcheck = errcheck(lambda result: result == 0)
_ReadProcessMemory.argtypes = [
    ctypes.wintypes.HANDLE,                 # hProcess
    ctypes.wintypes.LPCVOID,                # lpBaseAddress
    ctypes.wintypes.LPVOID,                 # lpBuffer
    ctypes.wintypes.SIZE_T,                 # nSize
    ctypes.POINTER(ctypes.wintypes.SIZE_T)] # lpNumberOfBytesRead


def read_process_memory(handle, base, size):
    buffer = (ctypes.c_byte * size)()
    result = _ReadProcessMemory(handle, base, buffer, size, None)
    return result, buffer


_WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
_WriteProcessMemory.restype = ctypes.wintypes.BOOL
_WriteProcessMemory.errcheck = errcheck(lambda result: result == 0)
_WriteProcessMemory.argtypes = [
    ctypes.wintypes.HANDLE,                 # hProcess
    ctypes.wintypes.LPCVOID,                # lpBaseAddress
    ctypes.wintypes.LPVOID,                 # lpBuffer
    ctypes.wintypes.SIZE_T,                 # nSize
    ctypes.POINTER(ctypes.wintypes.SIZE_T)] # lpNumberOfBytesWritten


def write_process_memory(handle, base, buffer):
    return _ReadProcessMemory(handle, base, buffer, ctypes.sizeof(buffer), None)


#_EnumProcessModules = win32process.EnumProcessModules
_EnumProcessModules = ctypes.windll.kernel32.K32EnumProcessModules
_EnumProcessModules.restype = ctypes.wintypes.BOOL
_EnumProcessModules.errcheck = errcheck(lambda result: result == 0)
_EnumProcessModules.argtypes = [
    ctypes.wintypes.HANDLE,                     # hProcess
    ctypes.POINTER(ctypes.wintypes.HMODULE),    # pointer to an hmodule array
    ctypes.wintypes.DWORD,                      # size of that array
    ctypes.wintypes.LPDWORD]                    # *out* expected minumum size of said array


def enum_process_modules(process):
    size = ctypes.c_int(0)
    _EnumProcessModules(process, (ctypes.wintypes.HMODULE * 1)(), 1, size)
    handles = (ctypes.wintypes.HMODULE * size.value)()
    result = _EnumProcessModules(process, handles, size.value, size)
    return result, handles


# https://docs.microsoft.com/en-us/windows/desktop/api/psapi/nf-psapi-getmoduleinformation
_K32GetModuleInformation = ctypes.windll.kernel32.K32GetModuleInformation
_K32GetModuleInformation.restype = ctypes.wintypes.BOOL
_K32GetModuleInformation.errcheck = errcheck(lambda result: result == 0)
_K32GetModuleInformation.argtypes = [
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.HMODULE,
    ctypes.POINTER(ctypes_helper.MODULEINFO),
    ctypes.wintypes.DWORD]


def get_module_information(process, module):
    info = ctypes_helper.MODULEINFO()
    result = _K32GetModuleInformation(process, module, info, ctypes.sizeof(ctypes_helper.MODULEINFO))
    return result, info


# https://docs.microsoft.com/en-us/windows/desktop/api/psapi/nf-psapi-getmodulebasenamew
_K32GetModuleBaseNameW = ctypes.windll.kernel32.K32GetModuleBaseNameW
_K32GetModuleBaseNameW.restype = ctypes.wintypes.DWORD
_K32GetModuleBaseNameW.errcheck = errcheck(lambda result: result == 0)
_K32GetModuleBaseNameW.argtypes = [
    ctypes.wintypes.HANDLE,                 # hProcess
    ctypes.wintypes.HMODULE,                # hMod
    ctypes.POINTER(ctypes.wintypes.LPWSTR), # pointer to wide, unicode string
    ctypes.wintypes.DWORD]                  # size of such string


def get_module_base_name(process, module):
    name = ctypes.create_unicode_buffer(256)
    result = _K32GetModuleBaseNameW(process, module, name, 256)
    return result, name