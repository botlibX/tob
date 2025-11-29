# This file is placed in the Public Domain.


from typing import Any, Generator


from .message import Message


class Broker:

    objects: dict[str, Any] = {}

    @staticmethod
    def add(obj: Any) -> None:
        Broker.objects[repr(obj)] = obj
        
    @staticmethod
    def all(attr: str) -> Generator[str, object]:
        for obj in Broker.objects.values():
            if attr and attr not in dir(obj):
                continue
            yield obj

    @staticmethod
    def get(origin: str) -> Any:
        return Broker.objects.get(origin, None)

    @staticmethod
    def like(origin: str) -> list[Any]:
        res = []
        for orig in Broker.objects:
            if origin.split()[0] in orig.split()[0]:
                res.append(orig)
        return res


def display(evt: Message) -> None:
    bot = Broker.get(evt.orig)
    if not bot:
        return
    bot.display(evt)


def __dir__():
    return (
        'Broker',
        'display'
    )
