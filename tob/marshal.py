# This file is placed in the Public Domain.


"encoder/decoder"


import json


from .objects import Object, construct


class Encoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            try:
                return vars(o)
            except TypeError:
                return repr(o)


def dump(obj, filepointer, *args, **kw):
    kw["cls"] = Encoder
    json.dump(obj, filepointer, *args, **kw)


def dumps(obj, *args, **kw):
    kw["cls"] = Encoder
    return json.dumps(obj, *args, **kw)


def hook(data):
    obj = Object()
    construct(obj, data)
    return obj


def load(filepointer, *args, **kw):
    kw["object_hook"] = hook
    return json.load(filepointer, *args, **kw)


def loads(string, *args, **kw):
    kw["object_hook"] = hook
    return json.loads(string, *args, **kw)


def __dir__():
    return (
        'dump',
        'dumps',
        'load',
        'loads'
    )
