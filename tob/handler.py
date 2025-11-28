# This file is placed in the Public Domain.


import queue


from typing import Callable


from .message import Message
from .threads import launch


class Handler:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()

    def callback(self, event: Message) -> None:
        func = self.cbs.get(event.kind, None)
        if not func:
            event.ready()
            return
        name = event.text and event.text.split()[0]
        event._thr = launch(func, event, name=name)

    def loop(self) -> None:
        while True:
            event = self.poll()
            if event is None:
                break
            event.orig = repr(self)
            self.callback(event)

    def poll(self) -> Message:
        return self.queue.get()

    def put(self, event: Message) -> None:
        self.queue.put(event)

    def register(self, kind: str, callback: Callable) -> None:
        self.cbs[kind] = callback

    def start(self) -> None:
        launch(self.loop)

    def stop(self) -> None:
        self.queue.put(None)


def __dir__():
    return (
        'Handler',
    )
