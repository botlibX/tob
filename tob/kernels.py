# This file is placed in the Public Domain.


import sys
import types


from .command import scan
from .configs import Config
from .loggers import level
from .methods import parse
from .package import Mods
from .threads import Thread, launch
from .workdir import Workdir


class Kernel:

    @staticmethod
    def configure() -> None:
        parse(Config, " ".join(sys.argv[1:]))
        level(Config.sets.get("level", "info"))
        Workdir.configure(Config.name)
        if "n" not in Config.opts:
            Mods.ignore = Config.ignore
        Mods.configure()


def scanner(
            names: list[str],
            init=False
           ) -> list[tuple[types.ModuleType, Thread]]:
    mods = []
    for name in names:
        mod = Mods.get(name)
        if not mod:
            continue
        scan(mod)
        if init and "init" in dir(mod):
            thr = launch(mod.init)
            mods.append((mod, thr))
    return mods


def __dir__():
    return (
        'Kernel',
        'scanner'
    )
