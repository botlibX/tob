# This file is placed in the Public Domain.


import logging
import queue
import threading
import _thread


from .brokers import Broker
from .handler import Handler
from .message import Message
from .threads import launch


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.olock = threading.RLock()
        self.oqueue = queue.Queue()
        self.silent = True
        Broker.add(self)

    def announce(self, text: str) -> None: ...

    def display(self, event: Message) -> None: ...

    def dosay(self, channel: str, text: str) -> None: ...

    def raw(self, text: str) -> None: ...

    def say(self, channel: str, text: str) -> None: ...

    def wait(self) -> None: ...


class Output(Client):

    def output(self) -> None: ...

    def start(self) -> None: ...

    def stop(self) -> None: ...


def __dir__():
    return (
        'Client',
        'Output'
    )
