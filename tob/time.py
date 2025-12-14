# This file is placed in the Public Domain.


"things are repeating"


import threading
import time


from .thread import Thread


class Time:

    @staticmethod
    def day(daystr):
        day = None
        month = None
        yea = None
        try:
            ymdre = re.search(r'(\d+)-(\d+)-(\d+)', daystr)
            if ymdre:
                (day, month, yea) = ymdre.groups()
        except ValueError:
            try:
                ymre = re.search(r'(\d+)-(\d+)', daystr)
                if ymre:
                    (day, month) = ymre.groups()
                    yea = time.strftime("%Y", time.localtime())
            except Exception as ex:
                raise NoDate(daystr) from ex
        if day:
            day = int(day)
            month = int(month)
            yea = int(yea)
            date = f"{day} {MONTH[month]} {yea}"
            return time.mktime(time.strptime(date, r"%d %b %Y"))
        raise NoDate(daystr)

    @staticmethod
    def hour(daystr):
        try:
            hmsre = re.search(r'(\d+):(\d+):(\d+)', str(daystr))
            hours = 60 * 60 * (int(hmsre.group(1)))
            hoursmin = hours  + int(hmsre.group(2)) * 60
            hmsres = hoursmin + int(hmsre.group(3))
        except AttributeError:
            pass
        except ValueError:
            pass
        try:
            hmre = re.search(r'(\d+):(\d+)', str(daystr))
            hours = 60 * 60 * (int(hmre.group(1)))
            hmsres = hours + int(hmre.group(2)) * 60
        except AttributeError:
            return 0
        except ValueError:
           return 0
        return hmsres

    @staticmethod
    def time(txt):
        try:
            target = Time.day(txt)
        except NoDate:
            target = Time.extract(Time.today())
        hour =  Time.hour(txt)
        if hour:
            target += hour
        return target

    @staticmethod
    def parse(txt):
        seconds = 0
        target = 0
        txt = str(txt)
        for word in txt.split():
            if word.startswith("+"):
                seconds = int(word[1:])
                return time.time() + seconds
            if word.startswith("-"):
                seconds = int(word[1:])
                return time.time() - seconds
        if not target:
            try:
                target = Time.day(txt)
            except NoDate:
               target = Time.extract(Time.today())
            hour = Time.hour(txt)
            if hour:
                target += hour
        return target

    @staticmethod
    def extract(daystr):
        previous = ""
        line = ""
        daystr = str(daystr)
        res = None
        for word in daystr.split():
            line = previous + " " + word
            previous = word
            try:
                res = Utils.extractdate(line.strip())
                break
            except ValueError:
                res = None
            line = ""
        return res

    @staticmethod
    def today():
        return str(datetime.datetime.today()).split()[0]


class Timy(threading.Timer):

    def __init__(self, sleep, func, *args, **kwargs):
        super().__init__(sleep, func)
        self.name = kwargs.get("name", Thread.name(func))
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
        self.name = thrname or kwargs.get("name", Thread.name(func))
        self.target = time.time() + self.sleep
        self.timer = None

    def run(self):
        self.timer.latest = time.time()
        self.func(*self.args)

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
        Thread.launch(self.start)
        super().run()


def __dir__():
    return (
        'Repeater',
        'Time',
        'Timed'
    )
