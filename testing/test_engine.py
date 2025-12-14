# This file is placed in the Public Domain.


"engine"


import unittest


from tob import Engine


class TestHandler(unittest.TestCase):

    def testcomposite(self):
        eng = Engine()
        self.assertEqual(type(eng), Engine)
