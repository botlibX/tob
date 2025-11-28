# This file is placed in the Public Domain.


import inspect


from types import ModuleType
from typing import Callable


from .brokers import display
from .message import Message
from .methods import parse


class Commands:

    cmds = {}
    names = {}

    @staticmethod
    def add(*args: list[Callable]) -> None:
       for func in args:
            name = func.__name__
            Commands.cmds[name] = func
            Commands.names[name] = func.__module__.split(".")[-1]

    @staticmethod
    def get(cmd: str) -> object:
        return Commands.cmds.get(cmd, None)


def command(evt: Message) -> None:
    parse(evt, evt.text)
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        display(evt)
    evt.ready()


def scan(module: object) -> None:
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in inspect.signature(cmdz).parameters:
            Commands.add(cmdz)


def __dir__():
    return (
        'Commands',
        'command',
        'scan'
    )
