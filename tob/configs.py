# This file is placed in the Public Domain.


from .objects import Default


class Config(Default):

    args: list[str] = []
    debug = False
    gets: dict[str, str] = {}
    ignore = ""
    index = 0
    local = False
    mods = False
    network = False
    sets: dict[str, str]  = {}
    silent: dict[str, str] = {}
    version = 0


def __dir__():
    return (
        'Config',
    )
