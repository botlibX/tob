# This file is placed in the Public Domain.


from .objects import Default


class Config(Default):

    debug = False
    gets: dict[str, str] = {}
    ignore = ""
    local = False
    mods = False
    name = ""
    network = False
    opts = ""
    sets: dict[str, str] = {}
    version = 0


def __dir__():
    return (
        'Config',
    )
