# This file is placed in the Public Domain.


"working directory"


import os


from typing import Literal


j = os.path.join


class Workdir:

    name: str
    wdr: str


def cdir(path) -> None:
    ...

def fqn(obj) -> str:
    ...

def getpath(obj) -> str:
    ...

def ident(obj) -> str:
    ...

def long(name) -> str:
    ...

def moddir() -> str:
    ...

def pidfile(filename) -> None:
    ...

def pidname(name) -> str:
    ...

def setwd(name, path=...) -> None:
    ...

def skel() -> str:
    ...

def store(pth=...) -> str:
    ...

def strip(pth, nmr=...) -> str:
    ...

def types() -> list[str]:
    ...

def __dir__() -> tuple[Literal['Workdir'], Literal['cdir'], Literal['fqn'], Literal['getpath'], Literal['ident'], Literal['j'], Literal['long'], Literal['moddir'], Literal['pidfile'], Literal['pidname'], Literal['setwd'], Literal['skel'], Literal['store'], Literal['strip'], Literal['types']]:
    ...
