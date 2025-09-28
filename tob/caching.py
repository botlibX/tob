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


def find(type, selector={}, removed=False, matching=False):
    type = long(type)
    for pth in fns(type):
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


def fns(type):
    path = store(type)
    for rootdir, dirs, _files in os.walk(path, topdown=False):
        for dirname in dirs:
            fullpath = os.path.join(rootdir, dirname)
            for filename in os.listdir(fullpath):
                yield os.path.join(fullpath, filename)


def last(object, selector={}):
    objects = sorted(find(fqn(object), selector), key=lambda x: fntime(x[0]))
    path = ""
    if objects:
        input = objects[-1]
        update(object, input[-1])
        path = input[0]
    return path


def read(object, path):
    with Cache.lock:
        with open(path, "r", encoding="utf-8") as filepointer:
            try:
                update(object, load(filepointer))
            except json.decoder.JSONDecodeError as exception:
                exeption.add_note(path)
                raise exception


def write(object, path=None):
    with Cache.lock:
        if path is None:
            path = getpath(object)
        cdir(path)
        with open(path, "w", encoding="utf-8") as filepointer:
            dump(object, filepointer, indent=4)
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
