# This file is placed in the Public Domain.


from .objects import Default


class Config(Default):

    args = []
    debug = False
    gets = {}
    ignore = ""
    index = 0
    local = False
    mods = False
    network = False
    sets  = {}
    silent = {}
    version = 0


def __dir__():
    return (
        'Config',
    )
