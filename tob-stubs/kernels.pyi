# This file is placed in the Public Domain.


import sys


from types import ModuleType

from .command import scan
from .configs import Config
from .loggers import level
from .methods import parse
from .package import Mods
from .threads import Thread, launch
from .workdir import Workdir


class Kernel:

    @staticmethod
    def configure() -> None: ...


def scanner(
            names: list[str],
            init=False
           ) -> list[tuple[ModuleType, Thread]]: ...


def __dir__():
    return (
        'Kernel',
        'scanner'
    )
