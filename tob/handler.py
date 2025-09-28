# This file is placed in the Public Domain.


"handle events"


import queue
import threading
import time
import _thread


from .threads import launch


class Event:

    def __init__(self):
        self._ready = threading.Event()
        self._thr = None
        self.args = []
        self.channel = ""
        self.command = ""
        self.ctime = time.time()
        self.origin = ""
        self.rest = ""
        self.result = {}
        self.text = ""
        self.type = "event"

    def done(self):
        self.reply("ok")

    def ready(self):
        self._ready.set()

    def reply(self, text):
        self.result[time.time()] = text

    def wait(self, timeout=None):
        try:
            self._ready.wait()
            if self._thr:
                self._thr.join(timeout)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


class Handler:

    def __init__(self):
        self.callbacks = {}
        self.queue = queue.Queue()
        self.ready = threading.Event()
        self.stopped = threading.Event()

    def available(self, event):
        return event.type in self.callbacks

    def callback(self, event):
        func = self.callbacks.get(event.type, None)
        if func:
            event._thr = launch(
                                func,
                                event,
                                name=event.text and event.text.split()[0]
                               )
        else:
            event.ready()

    def loop(self):
        while not self.stopped.is_set():
            try:
                event = self.poll()
                if event is None or self.stopped.is_set():
                    break
                event.origin = repr(self)
                self.callback(event)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    def poll(self):
        return self.queue.get()

    def put(self, event):
        self.queue.put(event)

    def register(self, type, callback):
        self.callbacks[type] = callback

    def start(self, daemon=True):
        self.stopped.clear()
        launch(self.loop, daemon=daemon)

    def stop(self):
        self.stopped.set()
        self.queue.put(None)


def __dir__():
    return (
        'Event',
        'Handler'
   )


__all__ = __dir__()
