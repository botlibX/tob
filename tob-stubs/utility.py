# This file is placed in the Public Domain.


import importlib.util
import os
import pathlib
import sys
import time
import types
import typing


from typing import Any

from .objects import Object
from .statics import TIMES


def cdir(path: str) -> None: ...


def check(text: str) -> bool: ...


def daemon(verbose: bool = False) -> None: ...


def elapsed(seconds: int, short: bool = True) -> str: ...


def extract_date(daystr: str) -> float: ...


def forever() -> None: ...


def getmain(name: str) -> Any: ...


def importer(name: str, pth: str = "") -> types.ModuleType | None: ...


def md5sum(path: str) -> str: ...


def pidfile(filename: str) -> None: ...


def privileges() -> None: ...


def spl(txt: str) -> list[str]: ...


def where(obj: Any) -> str: ...


def wrap(func: types.FunctionType) -> None: ...


def wrapped(func: types.FunctionType) -> None: ...


def __dir__():
    return (
        'cdir',
        'check',
        'daemon',
        'elapsed',
        'extract_date',
        'forever',
        'getmain',
        'importer',
        'md5sum',
        'pidfile',
        'privileges',
        'spl',
        'where',
        'wrap',
        'wrapped'
   )
