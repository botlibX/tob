# This file is placed in the Public Domain.


import os
import sys
import unittest


sys.path.insert(0, ".")


from tob.caching import Cache, workdir, write
from tob.objects import Object


import tob.caching


Cache.workdir = ".test"


ATTRS1 = (
    'Cache',
    'addpath',
    'find',
    'getpath',
    'kinds',
    'last',
    'persist',
    'read',
    'skel',
    'strip',
    'syncpath',
    'workdir',
    'write'
)


TARGET = tob.caching


class TestStorage(unittest.TestCase):

    def test_constructor(self):
        obj = Cache()
        self.assertTrue(type(obj), Cache)

    def test__class(self):
        obj = Cache()
        clz = obj.__class__()
        self.assertTrue('Cache' in str(type(clz)))

    def test_dirmodule(self):
        self.assertEqual(
                         dir(TARGET),
                         list(ATTRS1)
                        )

    def test_module(self):
        self.assertTrue(Cache().__module__, 'Cache')

    def test_save(self):
        obj = Object()
        opath = write(obj)
        print(opath)
        self.assertTrue(os.path.exists(os.path.join(workdir(), "store", opath)))
