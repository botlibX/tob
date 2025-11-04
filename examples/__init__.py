# This file is placed in the Public Domain.


"modules"


import importlib
import importlib.util
import os
import sys


path = os.path.dirname(__file__)
pkgname = path.split(os.sep)[-1]


def importer(name, pth):
    if not os.path.exists(pth):
        return
    spec = importlib.util.spec_from_file_location(name, pth)
    if not spec or not spec.loader:
        return
    mod = importlib.util.module_from_spec(spec)
    if not mod:
        return
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def modules():
    mods = []
    if os.path.exists(path):
        return sorted([
                x[:-3].split(".")[-1] for x in os.listdir(path)
                if x.endswith(".py") and not x.startswith("__")
               ])


for name in modules():
    pth = os.path.join(path, name + ".py")
    nme = pkgname + "." + name
    mod = importer(nme, pth)
    if mod:
        locals()[nme] = mod
