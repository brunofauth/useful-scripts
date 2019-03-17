from importlib import reload
from pprint import pprint


def info(obj):
    pprint(list(a for a in dir(obj) if a[0] != "_"))
