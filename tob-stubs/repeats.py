# This file is placed in the Public Domain.


import threading
import time


from .methods import name
from .threads import launch


class Timy(threading.Timer):

    def __init__(self, sleep, func, *args, **kwargs):
        super().__init__(sleep, func)
        self.name = kwargs.get("name", name(func))
        self.sleep = sleep
        self.state = {}
        self.state["latest"] = time.time()
        self.state["starttime"] = time.time()
        self.starttime = time.time()


class Timed:

    def __init__(self, sleep, func, *args, thrname="", **kwargs):
        self.args = args
        self.func = func
        self.kwargs = kwargs
        self.sleep = sleep
        self.name = thrname or kwargs.get("name", name(func))
        self.target = time.time() + self.sleep
        self.timer = None

    def run(self) -> None: ...

    def start(self) -> None: ...

    def stop(self) -> None: ...


class Repeater(Timed):

    def run(self) -> None: ...


def __dir__():
    return (
        'Repeater',
        'Timed'
    )
