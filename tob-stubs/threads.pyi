# This file is placed in the Public Domain.


import logging
import os
import queue
import threading
import time
import types
import typing
import _thread


from .methods import name


class Thread(threading.Thread):

    def __init__(self, func, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, None, (), daemon=daemon)
        self.event = None
        self.name = kwargs.get("name", name(func))
        self.queue = queue.Queue()
        self.result = None
        self.starttime = time.time()
        self.stopped = threading.Event()
        self.queue.put((func, args))

    def __iter__(self):
        return self

    def __next__(self):
        yield from dir(self)

    def join(self, timeout: float | None = 0.0) -> None: ...

    def run(self) -> None: ...


def launch(
           func: typing.Callable,
           *args,
           **kwargs
          ) -> Thread: ...


def threadhook(args) -> None: ...


def __dir__():
    return (
        'Thread',
        'launch',
        'threadhook'
    )
    