# This file is placed in the Public Domain.


import logging
import os
import sys
import threading
import _thread


from .threads import launch
from .utility import importer, md5sum, spl


lock = threading.RLock()


class Mods:

    ignore = "mbx,rst,udp,web"
    md5s = {}
    mod = os.path.join(os.path.dirname(__file__), "modules")
    package = __name__.split(".", maxsplit=1)[0] + "." + "modules"


def getmod(name, path=None):
    with lock:
        mname = Mods.package + "." +  name
        module = sys.modules.get(mname, None)
        if module:
            return module
        if not path:
            path = Mods.mod
        pth = os.path.join(path, f"{name}.py")
        if os.path.exists(pth) and name != "tbl":
            if Mods.md5s and md5sum(pth) != Mods.md5s.get(name, None):
                logging.warning("md5 error on %s", pth.split(os.sep)[-1])
        return importer(mname, pth)


def inits(names):
    modz = []
    for name in sorted(spl(names)):
        try:
            module = getmod(name)
            if not module:
                continue
            if "init" in dir(module):
                thr = launch(module.init)
                modz.append((module, thr))
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()
    return modz


def modules():
    if not os.path.exists(Mods.mod):
        return []
    return list({
            x[:-3] for x in os.listdir(Mods.mod)
            if x.endswith(".py") and not x.startswith("__") and
            x[:-3] not in spl(Mods.ignore)
           })


def sums(checksum):
    pth = os.path.join(Mods.mod, "tbl.py")
    if not os.path.exists(pth):
        logging.info("table is not there.")
        return
    elif checksum and md5sum(pth) != checksum:
        logging.warning("table checksum error.")
        return
    tbl = getmod("tbl")
    if tbl:
        if "MD5" in dir(tbl):
            Mods.md5s.update(tbl.MD5)


def __dir__():
    return (
        'Mods',
        'getmod',
        'init',
        'modules',
        'sums'
    )
