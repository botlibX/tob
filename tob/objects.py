# This file is placed in the Public Domain.


"a clean namespace."


import json


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


class Encoder(json.JSONEncoder):

    def default(self, object):
        if isinstance(object, dict):
            return object.items()
        if isinstance(object, Object):
            return vars(object)
        if isinstance(o, list):
            return iter(object)
        try:
            return json.JSONEncoder.default(self, object)
        except TypeError:
            try:
                return vars(object)
            except TypeError:
                return repr(object)


def dump(object, filepointer, *args, **kw):
    kw["cls"] = Encoder
    json.dump(object, filepointer, *args, **kw)


def dumps(object, *args, **kw):
    kw["cls"] = Encoder
    return json.dumps(object, *args, **kw)


def hook(data):
    object = Object()
    construct(object, data)
    return object


def load(filepointer, *args, **kw):
    kw["object_hook"] = hook
    return json.load(filepointer, *args, **kw)


def loads(string, *args, **kw):
    kw["object_hook"] = hook
    return json.loads(string, *args, **kw)



def __dir__():
    return (
        'Object',
        'construct',
        'dump',
        'dumps',
        'items',
        'keys',
        'load',
        'loads',
        'update',
        'values'
    )


__all__ = __dir__()
