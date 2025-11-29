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
        self.args = []
        self.cmd = ""
        self.index = 0
        self.kind = "event"
        self.opts = ""
        self.orig = ""
        self.rest = ""
        self.text = ""
        
    def ready(self) -> None: ...

    def reply(self, text: str) -> None: ...

    def wait(self, timeout: float = 0.0): ...


def __dir__():
    return (
        'Message',
    )
