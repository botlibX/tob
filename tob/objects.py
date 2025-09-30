# This file is placed in the Public Domain.


"a clean namespace"


class Object:

    def __contains__(self, key):
        return key in dir(self)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


def construct(object, *args, **kwargs):
    if args:
        val = args[0]
        if isinstance(val, zip):
            update(object, dict(val))
        elif isinstance(val, dict):
            update(object, val)
        elif isinstance(val, Object):
            update(object, vars(val))
    if kwargs:
        update(object, kwargs)


def items(object):
    if isinstance(object, dict):
        return object.items()
    return object.__dict__.items()


def keys(object):
    if isinstance(object, dict):
        return object.keys()
    return object.__dict__.keys()


def update(object, data, empty=True):
    for key, value in items(data):
        if not empty and not value:
            continue
        setattr(object, key, value)

def values(object):
    if isinstance(object, dict):
        return object.values()
    return object.__dict__.values()


def __dir__():
    return (
        'Object',
        'construct',
        'items',
        'keys',
        'update',
        'values'
    )
