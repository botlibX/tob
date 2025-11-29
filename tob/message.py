# This file is placed in the Public Domain.


import threading
import time


from .objects import Default


class Message(Default):

    def __init__(self):
        super().__init__()
        self._ready = threading.Event()
        self._result = {}
        self._thr = None
        self.kind = "event"
        self.orig = ""

    def ready(self) -> None:
        self._ready.set()

    def reply(self, text: str) -> None:
        self._result[time.time()] = text

    def wait(self, timeout: float = 0.0):
        self._ready.wait(timeout or None)
        if self._thr:
            self._thr.join(timeout)


def __dir__():
    return (
        'Message',
    )
