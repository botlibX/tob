# This file is placed in the Public Domain.


"encoder/decoder"


import json


from .objects import Object, construct


class Encoder(json.JSONEncoder):

    def default(self, object):
        if isinstance(object, dict):
            return object.items()
        if isinstance(object, Object):
            return vars(object)
        if isinstance(object, list):
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
        'dump',
        'dumps',
        'load',
        'loads'
    )
