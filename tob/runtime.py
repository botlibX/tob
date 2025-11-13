# This file is placed in thew Public Domain.


"runtime"



from .objects import Default
from .package import Mods
from .persist import Workdir
from .utility import where


class Config(Default):

    name = "tob"
    opts = ""
    sets = {}
    sleep = 60
    version = 141


def boot(name):
    Config.name = name
    Mods.ignore = ["mbx", "udp", "web", "rst"]
    Mods.add(f"{Config.name}.modules", os.path.join(where(Default), "modules"))
    Mods.add("mods", "mods")
    Workdir.wdr = os.path.expanduser(f"~/.{Config.name}")
