# This file is placed in the Public Domain.


from .objects import Default


class Config(Default):

    args: list[str] = []
    cmd = ""
    debug = False
    gets: dict[str, str] = {}
    index = 0
    init = ""
    ignore = ""
    local = False
    mods = False
    name = ""
    network = False
    opts = ""
    otxt = ""
    rest = ""
    sets: dict[str, str] = {}
    silent: dict[str, str] = {}
    text = ""
    version = 0


def __dir__():
    return (
        'Config',
    )
