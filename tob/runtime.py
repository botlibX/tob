# This file is placed in the Public Domain.


"all things runtime"


import json
import logging
import os
import os.path
import sys
import time


from .clients import Client
from .command import Commands, command, scanner, table
from .methods import parse
from .handler import Event
from .objects import update
from .workdir import Workdir, pidname, setwd
from .package import Mods, getmod, inits, modules, sums
from .utility import daemon, forever, level, md5sum, pidfile
from .utility import privileges


CHECKSUM = "b740892adad235295db24945c18bdc98"
NAME = Workdir.name


class Config:

    debug = False
    default = "irc,mdl,rss"
    gets = {}
    ignore = "mbx,rst,udp,web"
    init  = ""
    level = "warn"
    mod = ""
    opts = ""
    otext = ""
    sets = {}
    verbose = False
    version = 102
    wdr = ""


class CLI(Client):

    def __init__(self):
        Client.__init__(self)
        self.register("command", command)

    def announce(self, text):
        self.raw(text)

    def raw(self, text):
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


"scripts"


def background():
    daemon("-v" in sys.argv)
    privileges()
    banner()
    boot(False)
    pidfile(pidname(NAME))
    inits(Config.init or Config.default)
    forever()


def console():
    import readline # noqa: F401
    boot()
    for _mod, thr in inits(Config.init):
        if "w" in Config.opts:
            thr.join(30.0)
    csl = Console()
    csl.start(daemon=True)
    forever()


def control():
    if len(sys.argv) == 1:
        return
    boot()
    Commands.add(md5)
    Commands.add(srv)
    Commands.add(tbl)
    csl = CLI()
    evt = Event()
    evt.origin = repr(csl)
    evt.type = "command"
    evt.text = Config.otext
    command(evt)
    evt.wait()


def service():
    privileges()
    banner()
    boot(False)
    pidfile(pidname(NAME))
    banner()
    inits(Config.init or Config.default)
    forever()


def boot(doparse=True):
    if doparse:
        parse(Config, " ".join(sys.argv[1:]))
        update(Config, Config.sets, empty=False)
        Workdir.wdr = Config.wdr or Workdir.wdr or os.path.expanduser(f"~/.{NAME}")
    if "v" in Config.opts:
        banner()
    level(Config.level)
    if 'e' in Config.opts:
        pkg = sys.modules.get(NAME)
        pth = pkg.__path__[0]
        pth = os.sep.join(pth.split(os.sep)[:-4])
        pth = os.path.join(pth, 'share', NAME,  'examples')
        Mods.mod = Config.mod = pth
        Mods.package = "mods"
    elif "m" in Config.opts:
        Mods.mod = Config.mod = "mods"
        Mods.package = "mods"
    else:
        Mods. mod = os.path.join(os.path.dirname(__file__), "modules")
        Mods.package = __name__.split(".", maxsplit=1)[0] + "." + "modules"
    Mods.ignore = Config.ignore
    if "a" in Config.opts:
        Config.init = ",".join(modules())
    #setwd(NAME)
    sums(CHECKSUM)
    table(CHECKSUM)
    Commands.add(cmd)
    Commands.add(ver)
    logging.info("workdir is %s", Workdir.wdr)


"commands"


def cmd(event):
    event.reply(",".join(sorted(Commands.names)))


def md5(event):
    tbl = getmod("tbl")
    if tbl:
        event.reply(md5sum(tbl.__file__))
    else:
        event.reply("table is not there.")


TXT = """[Unit]
Description=%s
After=network-online.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%s -s

[Install]
WantedBy=multi-user.target"""


def srv(event):
    import getpass
    name = getpass.getuser()
    event.reply(TXT % (NAME.upper(), name, name, name, NAME))


def tbl(event):
    Commands.names = {}
    scanner()
    event.reply("# This file is placed in the Public Domain.")
    event.reply("")
    event.reply("")
    event.reply(f"NAMES = {json.dumps(Commands.names, indent=4, sort_keys=True)}")
    event.reply("")
    event.reply("MD5 = {")
    for module in scanner():
        event.reply(f'    "{module.__name__.split(".")[-1]}": "{md5sum(module.__file__)}",')
    event.reply("}")


def ver(event):
    event.reply(f"{NAME.upper()} {Config.version}")


"utilities"


def banner():
    tme = time.ctime(time.time()).replace("  ", " ")
    output("%s %s since %s (%s)" % (NAME.upper(), Config.version, tme, Config.level.upper()))


def check(text):
    args = sys.argv[1:]
    for arg in args:
        if not arg.startswith("-"):
            continue
        for char in text:
            if char in arg:
                return True
    return False


def output(text):
    print(text)
    sys.stdout.flush()


"runtime"


def wrapped(function):
    try:
        function()
    except (KeyboardInterrupt, EOFError):
        output("")


def wrap(function):
    import termios
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        wrapped(function)
    finally:
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def main():
    if check("c"):
        wrap(console)
    elif check("d"):
        background()
    elif check("s"):
        wrapped(service)
    else:
        wrapped(control)


if __name__ == "__main__":
    main()
