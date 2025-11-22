# This file is placed in the Public Domain.


from .objects import Default
from .package import configure as pconf
from .workdir import configure as wconf


class Config(Default):

    name = "nixt"
    version = 440


def configure(name, version, ignore=None, local=False):
    Config.name = name
    Config.version = version
    wconf(name)
    pconf(f"{name}.modules", ignore, local)


def __dir__():
    return (
        'Config',
    )
