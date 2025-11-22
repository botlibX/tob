# This file is placed in the Public Domain.


import threading
import time


from .configs import Default


class Message(Default):

    def __init__(self):
        super().__init__()
        self._ready = threading.Event()
        self.result = {}
        self.kind = "event"


def ready(msg):
    msg._ready.set()


def reply(msg, text):
    msg.result[time.time()] = text


def wait(msg, timeout=None):
    msg._ready.wait()
    if msg._thr:
        msg._thr.join(timeout)


def __dir__():
    return (
        'Message',
        'ready',
        'reply',
        'wait'
   )
