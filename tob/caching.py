# This file is placed in the Public Domain.


"cache objects on disk"


import json.decoder
import os
import threading


from .methods import fqn, deleted, search
from .objects import Object, dump, load, update
from .workdir import getpath, long, store
from .utility import cdir, fntime


class Cache:

    lock = threading.RLock()
    objects = {}

    @staticmethod
    def add(path, object):
        Cache.objects[path] = object

    @staticmethod
    def get(path):
        return Cache.objects.get(path, None)

    @staticmethod
    def update(path, object):
        if not object:
            return
        if path in Cache.objects:
            update(Cache.objects[path], object)
        else:
            Cache.add(path, object)


def find(clz, selector={}, removed=False, matching=False):
    clz = long(clz)
    for pth in fns(clz):
        object = Cache.get(pth)
        if not object:
            object = Object()
            read(object, pth)
            Cache.add(pth, object)
        if not removed and deleted(object):
            continue
        if selector and not search(object, selector, matching):
            continue
        yield pth, object


def fns(clz):
    pth = store(clz)
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        for dname in dirs:
            ddd = os.path.join(rootdir, dname)
            for fll in os.listdir(ddd):
                yield os.path.join(ddd, fll)


def last(object, selector={}):
    result = sorted(find(fqn(object), selector), key=lambda x: fntime(x[0]))
    res = ""
    if result:
        inp = result[-1]
        update(object, inp[-1])
        res = inp[0]
    return res


def read(object, path):
    with Cache.lock:
        with open(path, "r", encoding="utf-8") as fpt:
            try:
                update(object, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex


def write(object, path=None):
    with Cache.lock:
        if path is None:
            path = getpath(object)
        cdir(path)
        with open(path, "w", encoding="utf-8") as fpt:
            dump(object, fpt, indent=4)
        Cache.update(path, object)
        return path


def __dir__():
    return (
        'Cache',
        'find',
        'last',
        'read',
        'write'
    )


__all__ = __dir__()
