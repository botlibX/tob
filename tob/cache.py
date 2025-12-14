# This file is placed in the Public Domain.


"disk cache"


from .object import Object


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


def __dir__():
    return (
        'Cache',
    )
