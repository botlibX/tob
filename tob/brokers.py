# This file is placed in the Public Domain.


class Broker:

    objects = {}


def add(obj):
    Broker.objects[repr(obj)] = obj


def get(origin):
    return Broker.objects.get(origin, None)


def all(attr=None):
    for obj in Broker.objects.values():
        if attr and attr not in dir(obj):
            continue
        yield obj


def like(origin):
    for orig in Broker.objects:
        if origin.split()[0] in orig.split()[0]:
            yield orig


def __dir__():
    return (
        'Broker',
        'add',
        'get',
        'all',
        'like'
    )
