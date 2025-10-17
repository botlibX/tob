# This file is placed in the Public Domain.


"module management"


from types import ModuleType
from typing import Any, Literal


NAME = ...
PATH = ...
lock = ...


class Mods:

    debug = ...
    dirs: dict[str, str]
    md5s: dict[str, str]

    @staticmethod
    def dir(name: str, path: str) -> None:
        ...
    

def getmod(name: str) -> ModuleType | None:
    ...

def inits(names: str) -> list[Any]:
    ...

def modules() -> list[Any]:
    ...

def setdirs(network: bool = False, mods: bool = False) -> None:
    ...

def sums(checksum) -> None:
    ...


def __dir__() -> tuple[Literal['Mods'], Literal['getmod'], Literal['importer'], Literal['inits'], Literal['md5sum'], Literal['modules'], Literal['setdirs'], Literal['sums']]:
    ...
