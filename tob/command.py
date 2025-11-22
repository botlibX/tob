# This file is placed in the Public Domain.


import inspect


from .brokers import getobj
from .methods import parse


class Commands:

    cmds = {}
    names = {}


def addcmd(*args):
    for func in args:
        name = func.__name__
        Commands.cmds[name] = func
        Commands.names[name] = func.__module__.split(".")[-1]


def getcmd(cmd):
    return Commands.cmds.get(cmd, None)


def command(evt):
    parse(evt, evt.text)
    func = getcmd(evt.cmd)
    if func:
        func(evt)
        bot = getobj(evt.orig)
        bot.display(evt)
    evt.ready()


def scan(module):
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in inspect.signature(cmdz).parameters:
            addcmd(cmdz)


def __dir__():
    return (
        'Comamnds',
        'command',
        'getcmd',
        'scan'
    )
