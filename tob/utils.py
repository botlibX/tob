# This file is placed in the Public Domain.


"dumpyard"


import datetime
import inspect
import os


from .object import Object


class Utils:

    @staticmethod
    def ident(obj):
        return os.path.join(Object.fqn(obj), *str(datetime.datetime.now()).split())

    @staticmethod
    def md5sum(path):
        import hashlib
        with open(path, "r", encoding="utf-8") as file:
            txt = file.read().encode("utf-8")
            return hashlib.md5(txt, usedforsecurity=False).hexdigest()

    @staticmethod
    def spl(txt):
        try:
           result = txt.split(",")
        except (TypeError, ValueError):
           result = []
        return [x for x in result if x]

    @staticmethod
    def where(obj):
        return os.path.dirname(inspect.getfile(obj))

    @staticmethod
    def wrapped(func):
        try:
            func()
        except (KeyboardInterrupt, EOFError):
            pass


def __dir__():
    return (
        'Utils',
    )
