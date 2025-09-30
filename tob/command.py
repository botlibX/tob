# This file is placed in the Public Domain.


"program your own commands"


import inspect
import logging
import os


from .brokers import Fleet
from .methods import parse
from .package import Mods, getmod, modules
from .utility import md5sum, spl


class Commands:

    commands = {}
    names = {}

    @staticmethod
    def add(function):
        name = function.__name__
        modname = function.__module__.split(".")[-1]
        Commands.commands[name] = function
        Commands.names[name] = modname

    @staticmethod
    def get(command):
        function = Commands.commands.get(command, None)
        if function:
            return function
        name = Commands.names.get(command, None)
        if not name:
            return
        module = getmod(name)
        if not module:
            return
        scan(module)
        return Commands.commands.get(command, None)


def command(evt):
    parse(evt)
    function = Commands.get(evt.command)
    if function:
        function(evt)
        Fleet.display(evt)
    evt.ready()


def scan(module):
    for key, command in inspect.getmembers(module, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in inspect.signature(command).parameters:
            Commands.add(command)


def scanner(names=""):
    res = []
    assert Mods.mods
    for nme in sorted(modules()):
        if names and nme not in spl(names):
            continue
        module = getmod(nme)
        if not module:
            continue
        scan(module)
        res.append(module)
    return res


def table(checksum=""):
    table = getmod("tbl")
    if table and "NAMES" in dir(table):
        Commands.names.update(table.NAMES)
    else:
        scanner()


def __dir__():
    return (
        'Commands',
        'command',
        'scan',
        'scanner',
        'table'
    )
