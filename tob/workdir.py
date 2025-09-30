# This file is placed in the Public Domain.


"working directory"


import os
import pathlib


from .methods import ident


class Workdir:

    name = __file__.rsplit(os.sep, maxsplit=2)[-2]
    wdr  = ""


def getpath(object):
    return store(ident(object))


def long(name):
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def moddir():
    assert Workdir.wdr
    return os.path.join(Workdir.wdr, "mods")


def pidname(name):
    assert Workdir.wdr
    return os.path.join(Workdir.wdr, f"{name}.pid")


def setwd(name, path=""):
    path = path or os.path.expanduser(f"~/.{name}")
    Workdir.wdr = Workdir.wdr or path
    skel()


def skel():
    result = ""
    if not os.path.exists(store()):
        pth = pathlib.Path(store())
        pth.mkdir(parents=True, exist_ok=True)
        pth = pathlib.Path(moddir())
        pth.mkdir(parents=True, exist_ok=True)
        result =  str(pth)
    return result


def store(path=""):
    assert Workdir.wdr
    return os.path.join(Workdir.wdr, "store", path)


def strip(path, nmr=2):
    return os.path.join(path.split(os.sep)[-nmr:])


def types():
    skel()
    return os.listdir(store())


def wdr(path):
    assert Workdir.wdr
    return os.path.join(Workdir.wdr, path)


def __dir__():
    return (
        'Workdir',
        'getpath',
        'long',
        'moddir',
        'pidname',
        'setwd',
        'store',
        'strip',
        'types',
        'wdr'
    )
