# This file is placed in the Public Domain.


"non-blocking"


import threading


from typing import Any, Generator, Literal, Self


class Thread(threading.Thread):

    def __init__(self, func, *args, daemon=..., **kwargs) -> None:
        ...
    
    def __iter__(self) -> Self:
        ...
    
    def __next__(self) -> Generator[str, Any, None]:
        ...
    
    def join(self, timeout=...) -> None:
        ...
    
    def run(self) -> None:
        ...
    


class Timy(threading.Timer):

    def __init__(self, sleep, func, *args, **kwargs) -> None:
        ...
    


class Timed:

    def __init__(self, sleep, func, *args, thrname=..., **kwargs) -> None:
        ...
    
    def run(self) -> None:
        ...
    
    def start(self) -> None:
        ...
    
    def stop(self) -> None:
        ...
    


class Repeater(Timed):

    def run(self) -> None:
        ...
    

def launch(func, *args, **kwargs) -> Thread:
    ...


def __dir__() -> tuple[Literal['Repeater'], Literal['Thread'], Literal['launch'], Literal['name']]:
    ...
