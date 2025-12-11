# This file is placed in the Public Domain.


"methods"


import unittest


from tob.methods import Methods
from tob.objects import Object


class TestMethods(unittest.TestCase):

    def testformat(self):
        o = Object()
        o.a = "b"
        self.assertEqual(Methods.fmt(o), 'a="b"')
