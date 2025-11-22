# This file is placed in the Public Domain.


from .objects import Object
from .package import configure as pconf
from .workdir import configure as wconf


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


class Config(Default):

    name = "tob"
    version = 150


def configure(name, version, ignore="", local=False):
    Config.name = name
    Config.version = version
    wconf(name)
    pconf(f"{name}.modules", ignore, local)


def __dir__():
    return (
        'Config',
        'Default'
    )
