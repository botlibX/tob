# This file is placed in the Public Domain.


"write your own commands"


from typing import Callable


from tob.handler import Event


class Commands:

    cmds: dict[str, Callable[[Event], None]]
    names: dict[str, str]

    @staticmethod
    def add(func: str) -> None:
        ...
    
    @staticmethod
    def get(cmd: str): # -> None:
        ...
    

def command(evt): # -> None:
    ...

def scan(module): # -> None:
    ...

def scanner(names=...): # -> list[Any]:
    ...

def table(checksum=...): # -> None:
    ...

def __dir__(): # -> tuple[Literal['Commands'], Literal['command'], Literal['scan'], Literal['scanner'], Literal['table']]:
    ...

