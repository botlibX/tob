# This file is placed in the Public Domain.


"client event handler"


import logging
import queue
import threading
import _thread


from .brokers import addobj
from .handler import Handler
from .threads import launch


class Client(Handler):

    def __init__(self):
        super().__init__()
        self.olock = threading.RLock()
        self.silent = True
        addobj(self)

    def announce(self, text):
        "announce text to all channels."
        if not self.silent:
            self.raw(text)

    def display(self, event):
        "display event results."
        with self.olock:
            for tme in event.result:
                txt = event.result.get(tme)
                self.dosay(event.channel, txt)

    def dosay(self, channel, text):
        "say called by display."
        self.say(channel, text)

    def raw(self, text):
        "raw output."
        raise NotImplementedError("raw")

    def say(self, channel, text):
        "say text in channel."
        self.raw(text)


class Output(Client):

    def __init__(self):
        super().__init__()
        self.oqueue = queue.Queue()

    def display(self, event):
        "display event result."
        raise NotImplementedError

    def output(self):
        "output loop."
        while True:
            event = self.oqueue.get()
            if event is None:
                self.oqueue.task_done()
                break
            self.display(event)
            self.oqueue.task_done()

    def start(self):
        "start loop."
        launch(self.output)

    def stop(self):
        "stop loop."
        self.oqueue.put(None)

    def wait(self):
        "wait for output to finish."
        try:
            self.oqueue.join()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


def __dir__():
    return (
        'Client',
        'Output'
    )
