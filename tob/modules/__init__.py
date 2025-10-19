# This file is placed in the Public Domain.


"modules"


import time


from tob.workdir import d, getname


STARTTIME = time.time()


class Config:

    debug = False
    default = ""
    gets = {}
    index = None
    init  = ""
    level = "warn"
    mod = d(__file__)
    name = getname(__file__, 3)
    opts = ""
    otxt = ""
    sets = {}
    sum = ""
    verbose = False
    version = 132
    wdr = ""


def __dir__():
    return (
        'STARTTIME',
        'Config'
    )
