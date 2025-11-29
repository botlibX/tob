# This file is placed in the Public Domain.


import datetime
import os
import types


from typing import Any, ItemsView, KeysView, ValuesView


class Reserved(Exception):

    pass


class Object:

    def __init__(self):
        super().__init__()
        self.__deleted__ = False

    def __contains__(self, key):
        return key in dir(self)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


def construct(obj: Object, *args, **kwargs) -> None: ...


def fqn(obj: Object) -> str: ...


def ident(obj: Object) -> str: ...


def items(obj: Object | dict[str, str]) -> ItemsView: ...


def keys(obj: Object | dict) -> KeysView: ...


def update(
           obj: Object,
           data: Object | dict[str, Any],
           empty: bool =True
          ) -> None: ...


def values(obj: Object) -> ValuesView: ...


def __dir__():
    return (
        'Default',
        'Object',
        'Reserved',
        'construct',
        'fqn',
        'getid',
        'ident',
        'items',
        'keys',
        'update',
        'values'
    )
        