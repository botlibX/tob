# This file is placed in the Public Domain.


import datetime
import os
import types
import typing


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


def construct(obj: Object, *args, **kwargs) -> None:
    if args:
        val = args[0]
        if isinstance(val, zip):
            update(obj, dict(val))
        elif isinstance(val, dict):
            update(obj, val)
        else:
            update(obj, vars(val))
    if kwargs:
        update(obj, kwargs)


def fqn(obj: Object) -> str:
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        tpe = type(obj)
        kin = f"{tpe.__module__}.{tpe.__name__}"
    return kin


def ident(obj: Object) -> str:
    return os.path.join(fqn(obj), *str(datetime.datetime.now()).split())


def items(obj: Object | dict[str, str]) -> typing.ItemsView:
    if isinstance(obj, dict):
        return obj.items()
    if isinstance(obj, types.MappingProxyType):
        return obj.items()
    return obj.__dict__.items()


def keys(obj: Object | dict) -> typing.KeysView:
    if isinstance(obj, dict):
        return obj.keys()
    return obj.__dict__.keys()


def update(
           obj: Object,
           data: Object | dict[str, typing.Any],
           empty: bool =True
          ) -> None:
    if isinstance(obj, type):
        for k, v in items(data):
            if isinstance(getattr(obj, k, None), types.MethodType):
                raise Reserved(k)
            setattr(obj, k, v)
    elif isinstance(obj, dict):
        for k, v in items(data):
            setattr(obj, k, v)
    else:
        for key, value in items(data):
            if not empty and not value:
                continue
            setattr(obj, key, value)


def values(obj: Object) -> typing.ValuesView:
    if isinstance(obj, dict):
        return obj.values()
    return obj.__dict__.values()


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
        