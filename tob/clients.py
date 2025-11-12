# This file is placed in the Public Domain.


import queue
import threading


from .command import Fleet
from .handler import Handler
from .objects import Default
from .threads import launch


class Config(Default):

    name = "tob"
    opts = ""
    sets = Default()
    version = 141


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.olock = threading.RLock()
        self.oqueue = queue.Queue()
        self.silent = True
        Fleet.add(self)

    def announce(self, text):
        if not self.silent:
            self.raw(text)

    def display(self, event):
        with self.olock:
            for tme in sorted(event.result):
                self.dosay(
                           event.channel,
                           event.result[tme]
                          )

    def dosay(self, channel, text):
        self.say(channel, text)

    def raw(self, text):
        raise NotImplementedError("raw")

    def say(self, channel, text):
        self.raw(text)

    def wait(self):
        self.oqueue.join()    


class Output(Client):

    def output(self):
        while True:
            event = self.oqueue.get()
            if event is None:
                self.oqueue.task_done()
                break
            self.display(event)
            self.oqueue.task_done()

    def start(self):
        launch(self.output)
        super().start()

    def stop(self):
        self.oqueue.put(None)
        super().stop()


class Pool:

    clients: list[Client] = []
    lock = threading.RLock()
    nrcpu = 1
    nrlast = 0

    @staticmethod
    def add(client):
        Pool.clients.append(client)

    @staticmethod
    def init(cls, nr, verbose=False):
        Pool.nrcpu = nr
        for _x in range(Pool.nrcpu):
            clt = cls()
            clt.start()
            Pool.add(clt)

    @staticmethod
    def put(event):
        with Pool.lock:
            if Pool.nrlast >= Pool.nrcpu-1:
                Pool.nrlast = 0
            clt = Pool.clients[Pool.nrlast]
            clt.put(event)
            Pool.nrlast += 1


def __dir__():
    return (
        'Client',
        'Fleet',
        'Output',
        'Pool'
   )
