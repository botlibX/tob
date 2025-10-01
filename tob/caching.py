# This file is placed in the Public Domain.


"cache objects"


import json.decoder
import os
import threading


from .marshal import dump, load
from .methods import fqn, deleted, search
from .objects import Object, update
from .workdir import getpath, long, store
from .utility import cdir, fntime


lock = threading.RLock()


class Cache:

    objects = {}

    @staticmethod
    def add(path, obj):
        Cache.objects[path] = obj

    @staticmethod
    def get(path):
        return Cache.objects.get(path, None)

    @staticmethod
    def update(path, obj):
        if not obj:
            return
        if path in Cache.objects:
            update(Cache.objects[path], obj)
        else:
            Cache.add(path, obj)


def find(typ, selector={}, removed=False, matching=False):
    typ = long(typ)
    for pth in fns(typ):
        obj = Cache.get(pth)
        if not obj:
            obj = Object()
            read(obj, pth)
            Cache.add(pth, obj)
        if not removed and deleted(obj):
            continue
        if selector and not search(obj, selector, matching):
            continue
        yield pth, obj


def fns(typ):
    path = store(typ)
    for rootdir, dirs, _files in os.walk(path, topdown=False):
        for dirname in dirs:
            fullpath = os.path.join(rootdir, dirname)
            for filename in os.listdir(fullpath):
                yield os.path.join(fullpath, filename)


def last(obj, selector={}):
    objs = sorted(find(fqn(obj), selector), key=lambda x: fntime(x[0]))
    path = ""
    if objs:
        value = objs[-1]
        update(obj, value[-1])
        path = value[0]
    return path


def read(obj, path):
    with lock:
        with open(path, "r", encoding="utf-8") as filepointer:
            try:
                update(obj, load(filepointer))
            except json.decoder.JSONDecodeError as exception:
                exception.add_note(path)
                raise exception


def write(obj, path=None):
    with lock:
        if path is None:
            path = getpath(obj)
        cdir(path)
        with open(path, "w", encoding="utf-8") as filepointer:
            dump(obj, filepointer, indent=4)
        Cache.update(path, obj)
        return path


def __dir__():
    return (
        'Cache',
        'find',
        'last',
        'read',
        'write'
    )
