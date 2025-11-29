# This file is placed in the Public Domain.


import os
import pathlib


from .objects import Object, ident


class Workdir:

    wdr = ""

    @staticmethod
    def configure(name: str) -> None:
        Workdir.wdr = os.path.expanduser(f"~/.{name}")
        skel()


def getpath(obj: Object) -> str:
    return store(ident(obj))


def long(name: str) -> str:
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def moddir(modname: str = "") -> str:
    return os.path.join(Workdir.wdr, modname or "mods")


def pidname(name: str) -> str:
    return os.path.join(Workdir.wdr, f"{name}.pid")


def skel() -> None:
    path = store()
    if os.path.exists(path):
        return
    pth = pathlib.Path(path)
    pth.mkdir(parents=True, exist_ok=True)
    pth = pathlib.Path(moddir())
    pth.mkdir(parents=True, exist_ok=True)


def store(fnm: str = "") -> str:
    return os.path.join(Workdir.wdr, "store", fnm)


def types() -> list[str]:
    skel()
    return os.listdir(store())


def __dir__():
    return (
        'Workdir',
        'getid',
        'getpath',
        'ident',
        'long',
        'moddir',
        'pidname',
        'skel',
        'store',
        'types'
    )
