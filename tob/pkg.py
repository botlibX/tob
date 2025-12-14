# This file is placed in the Public Domain.


"multiple directory modules"


import os


from .config import Main
from .path   import Workdir
from .utils  import Utils


class Mods:

    dirs = {}
    modules = {}
    package = __spec__.parent or ""
    path = os.path.dirname(__spec__.loader.path)

    @staticmethod
    def add(name, path):
        Mods.dirs[name] = path

    @staticmethod
    def addpkg(pkg):
        Mods.add(pkg.__name__, pkg.__path__[0])

    @staticmethod
    def get(name):
        if name in Mods.modules:
            return Mods.modules.get(name)
        mname = ""
        pth = ""
        for packname, path in Mods.dirs.items():
            modpath = os.path.join(path, name + ".py")
            if not os.path.exists(modpath):
                continue
            pth = modpath
            mname = f"{packname}.{name}"
            break
        if not mname:
            return
        mod = Utils.importer(mname, pth)
        if not mod:
            return
        Mods.modules[name] = mod
        return mod

    @staticmethod
    def list():
        mods = []
        for name, path in Mods.dirs.items():
            if not os.path.exists(path):
                continue
            mods.extend([
                x[:-3] for x in os.listdir(path)
                if x.endswith(".py") 
                and not x.startswith("__")
                and name not in Utils.spl(Main.ignore)
            ])
        return ",".join(sorted(mods)).strip()

    @staticmethod
    def mods(names):
        return [Mods.get(x) for x in sorted(Utils.spl(names)) if x not in Utils.spl(Main.ignore)]


def __dir__():
    return (
        'Mods',
    )
