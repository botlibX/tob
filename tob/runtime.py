# This file is placed in the Public Domain.


"runtime scripts"


import inspect
import json
import logging
import os
import sys
import time


from .clients import CLI, Console
from .command import Commands, command, scanner, table 
from .methods import parse
from .objects import update
from .handler import Event
from .package import Mods, inits, modules, sums
from .workdir import Workdir
from .utility import check, forever, level, md5sum, output


CHECKSUM = ""
NAME = Workdir.name


class Config:

    debug = False
    default = "irc,rss"
    gets = {}
    ignore = ""
    init  = ""
    level = "warn"
    mod = ""
    opts = ""
    otext = ""
    sets = {}
    verbose = False
    version = 102
    wdr = ""


class CLI(CLI):

    def raw(self, text):
        output(text.encode('utf-8', 'replace').decode("utf-8"))


class Console(Console):

    def raw(self, text):
        output(text.encode('utf-8', 'replace').decode("utf-8"))


def background():
    daemon("-v" in sys.argv)
    privileges()
    banner()
    boot(False)
    pidfile(pidname(NAME))
    inits(Config.init or Config.default)
    forever()


def boot(doparse=True):
    if doparse:
        parse(Config, " ".join(sys.argv[1:]))
        update(Config, Config.sets, empty=False)
        Workdir.wdr = Config.wdr or Workdir.wdr or os.path.expanduser(f"~/.{NAME}")
    if "v" in Config.opts:
        banner()
    if "a" in Config.opts:
        Config.init = ",".join(modules())
    level(Config.level)
    sums(CHECKSUM)
    table(CHECKSUM)
    Commands.add(cmd)
    logging.info("workdir is %s", Workdir.wdr)


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
    Commands.add(ver)
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


"utilities"


def banner():
    tme = time.ctime(time.time()).replace("  ", " ")
    output("%s %s since %s (%s)" % (NAME.upper()[::-1], Config.version, tme, Config.level.upper()))


"commands"


def cmd(event):
    event.reply(",".join(sorted(Commands.names)))


def md5(event):
    tbl = getmod("tbl")
    if tbl:
        event.reply(md5sum(tbl.__file__))
    else:
        event.reply("table is not there.")


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
    event.reply("")
    event.reply("MD5 = {")
    for module in scanner():
        event.reply(f'    "{module.__name__.split(".")[-1]}": "{md5sum(module.__file__)}",')
    event.reply("}")


def ver(event):
    event.reply(f"{NAME.upper()} {Config.version}")


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


"main"


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
