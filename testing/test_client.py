# This file is placed in the Public Domain.


"clients"


import unittest


from tob import Client, Event


def hello(event):
    event.reply("hello")
    event.ready()


clt = Client()
clt.register("hello", hello)
clt.start()


class TestHandler(unittest.TestCase):

    def test_loop(self):
        e = Event()
        e.kind = "hello"
        clt.put(e)
        e.wait()
        self.assertTrue(True)
