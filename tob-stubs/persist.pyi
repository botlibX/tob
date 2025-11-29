# This file is placed in the Public Domain.


import threading
import typing


from .objects import Object


lock = threading.RLock()


class Cache:

    objects: dict[str, typing.Any] = {}

    @staticmethod
    def add(path: str, obj: Object | dict[str, typing.Any]) -> None: ...

    @staticmethod
    def get(path: str) -> Object | None: ...

    @staticmethod
    def sync(path: str, obj: Object | dict[str, typing.Any]) -> None: ...


def attrs(kind: str) -> list[str]: ...


def deleted(obj: Object): ...


def find(
         kind: str,
         selector: dict = {},
         removed: bool = False,
         matching=False
        ) -> typing.Generator[tuple[str, Object | dict[typing.Any, typing.Any]]]: ...


def fns(kind: str) -> typing.Generator[str]: ...


def fntime(daystr: str) -> float: ...


def last(obj: Object, selector: dict = {}) -> str: ...


def read(obj: Object, path: str) -> None: ...


def search(
           obj: Object,
           selector: dict = {},
           matching: bool =False
          ) -> bool: ...


def write(obj: Object, path: str = ""): ...


def __dir__():
    return (
        'Cache',
        'attrs',
        'deleted',
        'find',
        'fns',
        'fntime',
        'last',
        'read',
        'search',
        'write'
    )
