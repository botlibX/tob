# This file is placed in the Public Domain.


"persistence through storage"


import json
import threading


from .objects import Object
from .serials import Json
from .workdir import Workdir


class Cache:

    objects = {}

    @staticmethod
    def add(path, obj):
        Cache.objects[path] = obj

    @staticmethod
    def get(path):
        return Cache.objects.get(path, None)

    @staticmethod
    def sync(path, obj):
        try:
            Object.update(Cache.objects[path], obj)
        except KeyError:
            Cache.add(path, obj)


class Disk:

    lock = threading.RLock()

    @staticmethod
    def read(obj, path):
        with Disk.lock:
            with open(path, "r", encoding="utf-8") as fpt:
                try:
                    Object.update(obj, Json.load(fpt))
                except json.decoder.JSONDecodeError as ex:
                    ex.add_note(path)
                    raise ex

    @staticmethod
    def write(obj, path=""):
        with Disk.lock:
            if path == "":
                path = Workdir.path(obj)
            Workdir.cdir(path)
            with open(path, "w", encoding="utf-8") as fpt:
                Json.dump(obj, fpt, indent=4)
            Cache.sync(path, obj)
            return path


def __dir__():
    return (
        'Cache',
        'Disk'
    )
