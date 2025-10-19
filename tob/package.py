# This file is placed in the Public Domain.


"module management"


import inspect
import logging
import os
import sys
import threading
import _thread


from tob.threads import launch
from tob.utility import importer, md5sum
from tob.workdir import Workdir, getname, j, moddir


NAME = getname(__file__, 1)


lock = threading.RLock()


class Mods:

    debug = False
    dirs = {}
    md5s = {}

    @staticmethod
    def dir(name, path):
        Mods.dirs[name] = path


def getmod(name):
    for nme, path in Mods.dirs.items():
        mname = nme + "." +  name
        module = sys.modules.get(mname, None)
        if module:
            return module
        pth = j(path, f"{name}.py")
        if Mods.md5s:
            if os.path.exists(pth) and name != "tbl":
                md5 = Mods.md5s.get(name, None)
                if md5sum(pth) != md5:
                    file = pth.split(os.sep)[-1]
                    logging.info("md5 error %s", file)
        mod = importer(mname, pth)
        if mod:
            return mod


def inits(names):
    modz = []
    for name in modules():
        if name not in names:
            continue
        try:
            module = getmod(name)
            if module and "init" in dir(module):
                thr = launch(module.init)
                modz.append((module, thr))
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()
    return modz


def modules():
    mods = []
    for name, path in Mods.dirs.items():
        if not os.path.exists(path):
            continue
        mods.extend([
            x[:-3] for x in os.listdir(path)
            if x.endswith(".py") and not x.startswith("__")
           ])
    return sorted(mods)


def sums(checksum):
    tbl = getmod("tbl")
    if not tbl:
        logging.info("no table")
        return
    if "MD5" in dir(tbl):
        Mods.md5s.update(tbl.MD5)


def __dir__():
    return (
        'Mods',
        'getmod',
        'importer',
        'inits',
        'md5sum',
        'modules',
        'sums'
    )
