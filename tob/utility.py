# This file is placed in the Public Domain.


"the dirty bag"


import hashlib
import logging
import importlib
import importlib.util
import os
import pathlib
import sys
import time
import _thread


DEBUG = False


FORMATS = [
    "%Y-%M-%D %H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%d-%m",
    "%m-%d",
]


LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'warn': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}


class Formatter(logging.Formatter):

    def format(self, record):
        record.module = record.module.upper()
        return logging.Formatter.format(self, record)


def cdir(path):
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def check(text):
    args = sys.argv[1:]
    for arg in args:
        if not arg.startswith("-"):
            continue
        for char in text:
            if char in arg:
                return True
    return False



def daemon(verbose=False):
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        os._exit(0)
    if not verbose:
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())
    os.umask(0)
    os.chdir("/")
    os.nice(10)


def elapsed(seconds, short=True):
    text = ""
    nsec = float(seconds)
    if nsec < 1:
        return f"{nsec:.2f}s"
    yea     = 365 * 24 * 60 * 60
    week    = 7 * 24 * 60 * 60
    nday    = 24 * 60 * 60
    hour    = 60 * 60
    minute  = 60
    yeas    = int(nsec / yea)
    nsec   -= yeas * yea
    weeks   = int(nsec / week)
    nsec   -= weeks * week
    nrdays  = int(nsec / nday)
    nsec   -= nrdays * nday
    hours   = int(nsec / hour)
    nsec   -= hours * hour
    minutes = int(nsec / minute)
    nsec   -= int(minute * minutes)
    sec     = int(nsec)
    if yeas:
        text += f"{yeas}y"
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        text += f"{nrdays}d"
    if short and text:
        return text.strip()
    if hours:
        text += f"{hours}h"
    if minutes:
        text += f"{minutes}m"
    if sec:
        text += f"{sec}s"
    text = text.strip()
    return text


def extract_date(daystr):
    daystr = daystr.encode('utf-8', 'replace').decode("utf-8")
    res = time.time()
    for fmat in FORMATS:
        try:
            res = time.mktime(time.strptime(daystr, fmat))
            break
        except ValueError:
            pass
    return res


def fntime(daystr):
    datestr = " ".join(daystr.split(os.sep)[-2:])
    datestr = datestr.replace("_", " ")
    if "." in datestr:
        datestr, rest = datestr.rsplit(".", 1)
    else:
        rest = ""
    timed = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
    if rest:
        timed += float("." + rest)
    return float(timed)


def forever():
    while True:
        try:
            time.sleep(0.1)
        except (KeyboardInterrupt, EOFError):
            break


def importer(name, path):
    module = None
    if not os.path.exists(path):
        return module
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        if spec:
            module = importlib.util.module_from_spec(spec)
            if module:
                sys.modules[name] = module
                if spec.loader:
                    spec.loader.exec_module(module)
                if DEBUG:
                    module.DEBUG = True
                logging.info("load %s", path)
    except Exception as ex:
        logging.exception(ex)
        _thread.interrupt_main()
    return module


def level(loglevel="debug"):
    if loglevel != "none":
        datefmt = "%H:%M:%S"
        format_short = "%(module).3s %(message)-76s"
        ch = logging.StreamHandler()
        ch.setLevel(LEVELS.get(loglevel))
        formatter = Formatter(fmt=format_short, datefmt=datefmt)
        ch.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(ch)


def md5sum(path):
    with open(path, "r", encoding="utf-8") as file:
        text = file.read().encode("utf-8")
        return hashlib.md5(text).hexdigest()


def output(text):
    print(text)
    sys.stdout.flush()


def pidfile(filename):
    if os.path.exists(filename):
        os.unlink(filename)
    path2 = pathlib.Path(filename)
    path2.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def privileges():
    import getpass
    import pwd
    pwnam2 = pwd.getpwnam(getpass.getuser())
    os.setgid(pwnam2.pw_gid)
    os.setuid(pwnam2.pw_uid)


def spl(text):
    try:
        result = text.split(",")
    except (TypeError, ValueError):
        result = [
            text,
        ]
    return [x for x in result if x]


def __dir__():
    return (
        'cdir',
        'check',
        'daemon',
        'elapsed',
        'extract_date',
        'fntime',
        'forever',
        'level',
        'md5sum',
        'output',
        'pidfile',
        'privileges',
        'spl'
    )
