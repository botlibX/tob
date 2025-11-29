# This file is placed in the Public Domain.


import typing


from .message import Message


class Broker:

    objects: dict[str, typing.Any] = {}

    @staticmethod
    def add(obj: typing.Any) -> None:
        Broker.objects[repr(obj)] = obj
        
    @staticmethod
    def all(attr: str) -> typing.Generator[str, object]:
        for obj in Broker.objects.values():
            if attr and attr not in dir(obj):
                continue
            yield obj

    @staticmethod
    def get(origin: str) -> typing.Any:
        return Broker.objects.get(origin, None)

    @staticmethod
    def like(origin: str) -> list[typing.Any]:
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
