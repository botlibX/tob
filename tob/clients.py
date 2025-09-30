# This file is placed in the Public Domain.


"handle client events"


import queue
import threading
import _thread


from .brokers import Fleet
from .command import command
from .handler import Event, Handler
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


class CLI(Client):

    def __init__(self):
        Client.__init__(self)
        self.register("command", command)

    def announce(self, text):
        self.raw(text)

    def raw(self, text):
        raise NotImplementedError("raw")
        output(text.encode('utf-8', 'replace').decode("utf-8"))


class Console(CLI):

    def announce(self, text):
        pass

    def callback(self, event):
        if not event.text:
            return
        super().callback(event)
        event.wait()

    def poll(self):
        evt = Event()
        evt.text = input("> ")
        evt.type = "command"
        return evt



def __dir__():
    return (
        'CLI',
        'Client',
        'Console',
        'Output'
   )
