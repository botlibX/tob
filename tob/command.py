# This file is placed in the Public Domain.


"write your own commands"


import importlib
import importlib.util
import inspect
import os
import sys


from .clients import Fleet
from .methods import parse
from .objects import Default


class Mods:

    dirs = {}

    @staticmethod
    def add(name, path=None):
        if path is None:
            path = name
        Mods.dirs[name] = path


class Commands:

    cmds = {}
    names = {}

    @staticmethod
    def add(*args):
        for func in args:
            name = func.__name__
            Commands.cmds[name] = func
            Commands.names[name] = func.__module__.split(".")[-1]

    @staticmethod
    def get(cmd):
        return Commands.cmds.get(cmd, None)


def command(evt):
    parse(evt, evt.txt)
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        Fleet.display(evt)
    evt.ready()


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


def modules(path):
    mods = []
    if not os.path.exists(path):
        return mods
    mods.extend([
            x[:-3] for x in os.listdir(path)
            if x.endswith(".py") and not x.startswith("__")
           ])
    return sorted(mods)


def scan(module):
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in inspect.signature(cmdz).parameters:
            Commands.add(cmdz)


def scanner(names=[]):
    for name, path in Mods.dirs.items():
        if names and name not in names:
            continue
        for nme in modules(path):
            modpath = os.path.join(path, nme + ".py")
            pkgname = path.split(os.sep)[-1]
            modname = ".".join((pkgname, nme))
            mod = importer(modname, modpath)
            if mod:
                scan(mod)


def __dir__():
    return (
        'Comamnds',
        'command',
        'importer',
        'modules',
        'scan',
        'scanner'
    )
