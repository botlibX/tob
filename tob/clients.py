# This file is placed in the Public Domain.


"handle client events"


import queue
import threading
import _thread


from .handler import Handler
from .threads import launch


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.olock = threading.RLock()
        Fleet.add(self)

    def announce(self, text):
        pass

    def display(self, event):
        with self.olock:
            for tme in sorted(event.result):
                self.dosay(event.channel, event.result[tme])

    def dosay(self, channel, text):
        self.say(channel, text)

    def raw(self, text):
        raise NotImplementedError("raw")

    def say(self, channel, text):
        self.raw(text)

    def wait(self):
        pass


class Output(Client):

    def __init__(self):
        Client.__init__(self)
        self.oqueue = queue.Queue()
        self.ostop = threading.Event()

    def oput(self, event):
        self.oqueue.put(event)

    def output(self):
        while not self.ostop.is_set():
            event = self.oqueue.get()
            if event is None:
                self.oqueue.task_done()
                break
            self.display(event)
            self.oqueue.task_done()

    def raw(self, text):
        raise NotImplementedError("raw")

    def start(self, daemon=True):
        self.ostop.clear()
        launch(self.output, daemon=daemon)
        super().start()

    def stop(self):
        self.ostop.set()
        self.oqueue.put(None)
        super().stop()

    def wait(self):
        try:
            self.oqueue.join()
        except Exception:
            _thread.interrupt_main()


class Fleet:

    clients = {}

    @staticmethod
    def add(client):
        if not client:
            return
        Fleet.clients[repr(client)] = client

    @staticmethod
    def all():
        return list(Fleet.clients.values())

    @staticmethod
    def announce(text):
        for client in Fleet.all():
            client.announce(text)

    @staticmethod
    def display(event):
        client = Fleet.get(event.origin)
        client.display(event)

    @staticmethod
    def get(origin):
        return Fleet.clients.get(origin, None)

    @staticmethod
    def say(origin, channel, text):
        client = Fleet.get(origin)
        client.say(channel, text)

    @staticmethod
    def shutdown():
        for client in Fleet.all():
            client.stop()
            client.wait()


def __dir__():
    return (
        'Client',
        'Fleet',
        'Output'
   )
