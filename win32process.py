import win32api, win32process, win32security
from win32con import PROCESS_ALL_ACCESS
import ctypes_helper
import winfunc
import ctypes
import code


# gotta adjust some yee yee ass privilege for openprocess to work
# token_handle = win32security.OpenProcessToken(win32api.GetCurrentProcess(),  win32security.TOKEN_ADJUST_PRIVILEGES)
# luid = win32security.LookupPrivilegeValue(None, win32security.SE_DEBUG_NAME)
# win32security.AdjustTokenPrivileges(token_handle, 0, [(luid, win32security.SE_PRIVILEGE_ENABLED)])
# win32api.CloseHandle(token_handle)


def getModules(process: int) -> dict:
    modules = {}
    for handle in winfunc.enum_process_modules(process)[1]:
        _, name = winfunc.get_module_base_name(process, handle)
        _, info = winfunc.get_module_information(process, handle)
        modules[name] = info
    return modules


class ProcessMemory(object):
    def __init__(self, pid, mod_buf_size=64):
        self.mod_buf_size = mod_buf_size
        self.handle = None
        self.pid = pid
    
    def __enter__(self):
        self.handle = winfunc.open_process(self.pid, flags=PROCESS_ALL_ACCESS)
        #self.modules = getModules(self.handle, self.mod_buf_size)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.handle is None:
            raise RuntimeError("There is no handle opened.")
        winfunc.close_handle(self.handle)
        self.handle = None
    
    def read(self, base: int, size: int) -> bytes:
        """Returns an array of SIZE bytes read, starting from BASE."""
        if self.handle is None:
            raise RuntimeError("There is no handle opened.")
        return winfunc.read_process_memory(self.handle, base, size)[1]
    
    def write(self, base: int, buffer: bytes, size: int) -> None:
        if self.handle is None:
            raise RuntimeError("There is no handle opened.")
        winfunc.write_process_memory(self.handle, base, buffer)


if __name__ == "__main__":
    code.interact(local=globals())