# This file is placed in the Public Domain.


import datetime
import os
import pathlib


class Workdir:

    wdr = ""


def cdir(path):
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def fqn(obj):
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def getpath(obj):
    return store(ident(obj))


def ident(obj):
    return os.path.join(fqn(obj), *str(datetime.datetime.now()).split())


def moddir(modname=None):
    return os.path.join(Workdir.wdr, modname or "mods")


def pidname(name):
    assert Workdir.wdr
    return os.path.join(Workdir.wdr, f"{name}.pid")


def skel():
    pth = pathlib.Path(store())
    pth.mkdir(parents=True, exist_ok=True)
    pth = pathlib.Path(moddir())
    pth.mkdir(parents=True, exist_ok=True)


def store(fnm=""):
    return os.path.join(Workdir.wdr, "store", fnm)


def types():
    return os.listdir(store())


def __dir__():
    return (
        'Workdir',
        'cdir',
        'fntime',
        'fqn',
        'fqn',
        'getpath',
        'ident',
        'skel',
        'types'
    )
