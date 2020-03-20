import contextlib
import functools
import threading
import requests
import inspect
import pprint
import sys
import io


def attrs(obj, show_private=False):
    pprint.pprint({attr: type(getattr(obj, attr)) for attr in dir(obj) if attr[0] != "_" or show_private})


def lazy_init(cls):
    sig = inspect.signature(cls.__init__)
    params = iter(sig.parameters.keys())
    self = next(params)
    body = "\n".join(f"    {self}.{param} = {param}" for param in params)
    exec(f"def __init__{sig}:\n" + body)
    functools.update_wrapper(locals()["__init__"], cls.__init__)
    cls.__init__ = locals()["__init__"]
    return cls


@contextlib.contextmanager
def bufferize_stdout():
    t = io.StringIO()
    try:
        with contextlib.redirect_stdout(t):
            yield
    finally:
        t.seek(0)
        sys.stdout.write(t.read())


def dlfile(url: str, output: str=None, chunk_size: int=1024 * 1024) -> None:
    with open(output, "wb") as file:
        req = requests.get(url, stream=True)
        if req.status_code != 200:
            raise RuntimeError(f"Download request returned code {req.status_code}.")
        for chunk in req.iter_content(chunk_size):
            file.write(chunk)


def thread(autostart=True, name=None, daemon=None):
    '''Decorator for making new thread when calling function.'''
    def _func(func):
        def _args(*args, **kwargs):
            t = threading.Thread(target=func, args=args,
                kwargs=kwargs, name=name, daemon=daemon)
            if autostart:
                t.start()
            return t
        return _args
    return _func


def first(iter, func=bool):
    '''Returns the first element from iter that returns True.'''
    for item in iter:
        if func(item):
            return item
    raise ValueError("No such item.")

