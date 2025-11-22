# This file is placed in the Public Domain.


import json
import threading


from .objects import Object, update
from .serials import dump, load
from .utility import cdir
from .workdir import getpath


lock = threading.RLock()


class Cache:

    objs = Object()


def add(path, obj):
    setattr(Cache.objs, path, obj)


def get(path):
    return getattr(Cache.objs, path, None)


def read(obj, path):
    with lock:
        with open(path, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex

def sync(path, obj):
    setattr(Cache.objs, path, obj)


def write(obj, path=None):
    with lock:
        if path is None:
            path = getpath(obj)
        cdir(path)
        with open(path, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        sync(path, obj)
        return path


def __dir__():
    return (
        'Cache',
        'add',
        'cdir',
        'get',
        'read',
        'update',
        'write'
    )
