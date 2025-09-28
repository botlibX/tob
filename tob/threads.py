# This file is placed in the Public Domain.


"run code non-blocking."


import logging
import queue
import threading
import time
import _thread


from .methods import name


class Thread(threading.Thread):

    def __init__(self, function, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, None, (), daemon=daemon)
        self.name = kwargs.get("name", name(function))
        self.queue = queue.Queue()
        self.result = None
        self.starttime = time.time()
        self.stopped = threading.Event()
        self.queue.put((function, args))

    def __iter__(self):
        return self

    def __next__(self):
        yield from dir(self)

    def join(self, timeout=None):
        result = None
        try:
            super().join(timeout)
            result = self.result
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()
        return result

    def run(self):
        function, args = self.queue.get()
        try:
            self.result = function(*args)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


class Timy(threading.Timer):

    def __init__(self, sleep, function, *args, **kwargs):
        super().__init__(sleep, function)
        self.name = kwargs.get("name", name(function))
        self.sleep = sleep
        self.state = {}
        self.state["latest"] = time.time()
        self.state["starttime"] = time.time()
        self.starttime = time.time()


class Timed:

    def __init__(self, sleep, function, *args, thrname="", **kwargs):
        self.args = args
        self.function = function
        self.kwargs = kwargs
        self.sleep = sleep
        self.name = thrname or kwargs.get("name", name(function))
        self.target = time.time() + self.sleep
        self.timer = None

    def run(self):
        self.timer.latest = time.time()
        self.function(*self.args)

    def start(self):
        self.kwargs["name"] = self.name
        timer = Timy(self.sleep, self.run, *self.args, **self.kwargs)
        timer.start()
        self.timer = timer

    def stop(self):
        if self.timer:
            self.timer.cancel()


class Repeater(Timed):

    def run(self):
        launch(self.start)
        super().run()


def launch(function, *args, **kwargs):
    thread = Thread(function, *args, **kwargs)
    thread.start()
    return thread


def __dir__():
    return (
        'Repeater',
        'Thread',
        'launch'
   )


__all__ = __dir__()
