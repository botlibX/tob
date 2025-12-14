# This file is placed in the Public Domain.


"disk persistence"


import json
import os
import threading
import time


from .cache  import Cache
from .json   import Json
from .object import Object
from .path   import Workdir


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
        'Disk',
        'Locate'
    )
