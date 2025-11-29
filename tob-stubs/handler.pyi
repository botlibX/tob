# This file is placed in the Public Domain.


import queue
import types


from .message import Message


class Handler:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()

    def callback(self, event: Message) -> None: ...

    def loop(self) -> None: ...

    def poll(self) -> Message: ...

    def put(self, event: Message) -> None: ...

    def register(self, kind: str, callback: types.FunctionType) -> None: ...

    def start(self) -> None: ...

    def stop(self) -> None: ...


def __dir__():
    return (
        'Handler',
    )
