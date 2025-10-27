# This file is placed in the Public Domain.


import unittest


from tob.marshal import dumps, loads
from tob.objects import Object


class TestDecoder(unittest.TestCase):

    def test_loads(self):
        obj = Object()
        obj.test = "bla"
        oobj = loads(dumps(obj))
        self.assertEqual(oobj["test"], "bla")

    def test_doctest(self):
        self.assertTrue(__doc__ is None)
