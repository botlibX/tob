# This file is placed in the Public Domain.


"modules management"


import hashlib
import importlib
import importlib.util
import logging
import os
import sys
import threading
import _thread


from .threads import launch


lock = threading.RLock()
name = __name__.split(".", maxsplit=1)[0]
path = os.path.dirname(__file__)


class Mods:

    debug = False
    md5s = {}
    mods = {}
    mods[name + ".modules"] = os.path.join(path, "modules")
    name = name
    path = path


def getmod(name):
    with lock:
        for nme, path in Mods.mods.items():
            mname = nme + "." +  name
            module = sys.modules.get(mname, None)
            if module:
                return module
            pth = os.path.join(path, f"{name}.py")
            if Mods.md5s and os.path.exists(pth) and name != "tbl":
                if md5sum(pth) != Mods.md5s.get(name, None):
                    logging.info("md5 error on %s", pth.split(os.sep)[-1])
            mod = importer(mname, pth)
            if not mod:
                continue
            return mod


def importer(name, pth):
    if not os.path.exists(pth):
        return
    try:
        spec = importlib.util.spec_from_file_location(name, pth)
        if spec:
            mod = importlib.util.module_from_spec(spec)
            if mod:
                sys.modules[name] = mod
                if spec.loader:
                    spec.loader.exec_module(mod)
                if Mods.debug:
                    mod.DEBUG = True
                logging.info("load %s", pth)
                return mod
    except Exception as ex:
        logging.exception(ex)
        _thread.interrupt_main()


def inits(names):
    modz = []
    for name in modules():
        if name not in names:
            continue
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


def md5sum(path):
    with open(path, "r", encoding="utf-8") as file:
        txt = file.read().encode("utf-8")
        return hashlib.md5(txt).hexdigest()


def modules():
    mods = []
    for name, path in Mods.mods.items():
        if not os.path.exists(path):
            continue
        mods.extend([
            x[:-3] for x in os.listdir(path)
            if x.endswith(".py") and not x.startswith("__")
           ])
    return sorted(mods)


def sums(checksum):
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
