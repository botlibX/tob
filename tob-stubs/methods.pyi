# This file is placed in the Public Domain.


import typing


from .configs import Config
from .message import Message
from .objects import Object


def edit(
         obj: Object,
         setter: dict[str, str],
         skip: bool = True
        ) -> None: ...


def fmt(
        obj: Object,
        args: list[str] = [],
        skip: list[str] = [],
        plain: bool = False,
        empty: bool = False
    ) -> str: ...


def name(obj: typing.Any): ...


def parse(obj: type[Config] | Message, text: str): ...


def __dir__():
    return (
        'edit',
        'fmt',
        'name',
        'parse'
    )
