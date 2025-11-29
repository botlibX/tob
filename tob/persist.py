# This file is placed in the Public Domain.


import json
import os
import threading
import time
import typing


from .objects import Object, fqn, items, keys, update
from .serials import dump, load
from .utility import cdir
from .workdir import getpath, long, store


lock = threading.RLock()


class Cache:

    objects: dict[str, typing.Any] = {}

    @staticmethod
    def add(path: str, obj: Object | dict[str, typing.Any]) -> None:
        Cache.objects[path] = obj

    @staticmethod
    def get(path: str) -> Object | None:
        return Cache.objects.get(path, None)

    @staticmethod
    def sync(path: str, obj: Object | dict[str, typing.Any]) -> None:
        if path not in Cache.objects:
            return Cache.add(path, obj)
        update(Cache.objects[path], obj)


def attrs(kind: str) -> list[str]:
    objs = list(find(kind))
    if objs:
        return list(keys(objs[0][1]))
    return []


def deleted(obj: Object):
    return "__deleted__" in dir(obj) and obj.__deleted__


def find(
         kind: str,
         selector: dict = {},
         removed: bool = False,
         matching=False
        ) -> typing.Generator[tuple[str, Object | dict[typing.Any, typing.Any]]]:
    if selector is None:
        selector = {}
    fullname = long(kind)
    for pth in fns(fullname):
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


def fns(kind: str) -> typing.Generator[str]:
    path = store(kind)
    for rootdir, dirs, _files in os.walk(path, topdown=True):
        for dname in dirs:
            if dname.count("-") != 2:
                continue
            ddd = os.path.join(rootdir, dname)
            for fll in os.listdir(ddd):
                yield os.path.join(ddd, fll)


def fntime(daystr: str) -> float:
    datestr = " ".join(daystr.split(os.sep)[-2:])
    datestr = datestr.replace("_", " ")
    if "." in datestr:
        datestr, rest = datestr.rsplit(".", 1)
    else:
        rest = ""
    timed = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
    if rest:
        timed += float("." + rest)
    return float(timed)


def last(obj: Object, selector: dict = {}) -> str:
    if selector is None:
        selector = {}
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x[0])
                   )
    res = ""
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        res = inp[0]
    return res


def read(obj: Object, path: str) -> None:
    with lock:
        with open(path, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex


def search(
           obj: Object,
           selector: dict = {},
           matching: bool =False
          ) -> bool:
    res = False
    for key, value in items(selector):
        val = getattr(obj, key, None)
        if not val:
            continue
        if matching and value == val:
            res = True
        elif str(value).lower() in str(val).lower():
            res = True
        else:
            res = False
            break
    return res


def write(obj: Object, path: str = ""):
    with lock:
        if path == "":
            path = getpath(obj)
        cdir(path)
        with open(path, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        Cache.sync(path, obj)
        return path


def __dir__():
    return (
        'Cache',
        'attrs',
        'deleted',
        'find',
        'fns',
        'fntime',
        'last',
        'read',
        'search',
        'write'
    )
