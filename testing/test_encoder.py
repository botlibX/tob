# This file is placed in the Public Domain.


import unittest


from tob import Json, Object


VALIDJSON = '{"test": "bla"}'


class TestEncoder(unittest.TestCase):

    def test_dumps(self):
        obj = Object()
        obj.test = "bla"
        self.assertEqual(Json.dumps(obj), VALIDJSON)
