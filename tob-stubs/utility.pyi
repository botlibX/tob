# This file is placed in the Public Domain.


"utilities"


import logging


from types import ModuleType
from typing import Any, Literal


FORMATS = ...
LEVELS = ...


class Formatter(logging.Formatter):

    def format(self, record) -> str:
        ...
    

def check(txt) -> bool:
    ...

def daemon(verbose=...) -> None:
    ...

def elapsed(seconds, short=...) -> str:
    ...

def extract_date(daystr) -> float:
    ...

def fntime(daystr) -> float:
    ...

def forever() -> None:
    ...

def importer(name, pth) -> ModuleType | None:
    ...

def level(loglevel=...) -> None:
    ...

def md5sum(path) -> str:
    ...

def privileges(): # -> None:
    ...

def spl(txt) -> list[Any]:
    ...


def __dir__() -> tuple[Literal['check'], Literal['daemon'], Literal['elapsed'], Literal['extract_date'], Literal['fntime'], Literal['forever'], Literal['importer'], Literal['level'], Literal['md5sum'], Literal['privileges'], Literal['spl']]:
    ...
