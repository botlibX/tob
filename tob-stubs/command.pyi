# This file is placed in the Public Domain.


import inspect
import types


from .brokers import display
from .message import Message
from .methods import parse


class Commands:

    cmds: dict[str, types.FunctionType] = {}
    names: dict[str, str] = {}

    @staticmethod
    def add(*args: types.FunctionType) -> None: ...

    @staticmethod
    def get(cmd: str) -> types.FunctionType | None: ...


def command(evt: Message) -> None: ...

def scan(module: types.ModuleType) -> None: ...


def __dir__():
    return (
        'Commands',
        'command',
        'scan'
    )
