# This file is placed in the Public Domain.


import inspect


from .brokers import get as bget
from .message import ready
from .methods import parse


class Commands:

    cmds = {}
    names = {}


def add(*args):
    for func in args:
        name = func.__name__
        Commands.cmds[name] = func
        Commands.names[name] = func.__module__.split(".")[-1]


def get(cmd):
    return Commands.cmds.get(cmd, None)


def command(evt):
    parse(evt, evt.text)
    func = get(evt.cmd)
    if func:
        func(evt)
        bot = bget(evt.orig)
        bot.display(evt)
    ready(evt)


def scan(module):
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in inspect.signature(cmdz).parameters:
            add(cmdz)


def __dir__():
    return (
        'Comamnds',
        'add',
        'get',
        'command',
        'scan'
    )
