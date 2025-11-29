# This file is placed in the Public Domain.


from typing import Any, Generator


from .message import Message


class Broker:

    objects: dict[str, Any] = {}

    @staticmethod
    def add(obj: Any) -> None: ...
        
    @staticmethod
    def all(attr: str) -> Generator[str, object]: ...

    @staticmethod
    def get(origin: str) -> Any: ...

    @staticmethod
    def like(origin: str) -> list[Any]: ...


def display(evt: Message) -> None: ...


def __dir__():
    return (
        'Broker',
        'display'
    )
