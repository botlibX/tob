# This file is placed in the Public Domain.


"object for a string"


from typing import Any, Generator, Literal


from tob.objects import Object


lock = ...


class Cache:

    objs: dict[str, Object]

    @staticmethod
    def add(path: str, obj: Object) -> None:
        ...
    
    @staticmethod
    def get(path: str) -> Object:
        ...
    
    @staticmethod
    def update(path: str, obj: Object) -> None:
        ...
    


def find(clz: str, selector=..., removed=..., matching=...) -> Generator[tuple[str, Object | Any], Any, None]:
    ...

def fns(clz) -> Generator[str, Any, None]:
    ...

def last(obj: Object, selector=...) -> str:
    ...

def read(obj: Object, path: str) -> None:
    ...

def write(obj, path=...) -> str:
    ...

def __dir__() -> tuple[Literal['Cache'], Literal['find'], Literal['last'], Literal['read'], Literal['write']]:
    ...
