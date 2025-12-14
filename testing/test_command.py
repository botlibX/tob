# This file is placed in the Public Domain.


"commands"


import unittest


from tob import Command


class TestCommands(unittest.TestCase):

    def test_construct(self):
        cmds = Command()
        self.assertEqual(type(cmds), Command)
