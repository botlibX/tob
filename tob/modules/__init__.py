# This file is placed in the Public Domain.


"modules"


from tob.workdir import d, getname


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

print(Config.mod)
print(Config.name)