# This file is placed in the Public Domain.


"methods"


import unittest


from tob.methods import fmt
from tob.objects import Object


class TestMethods(unittest.TestCase):

    def testformat(self):
        o = Object()
        o.a = "b"
        self.assertEqual(fmt(o), 'a="b"')
