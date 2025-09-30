# This file is placed in the Public Domain.


"loading on demand"


import inspect
import logging
import os
import sys
import threading
import _thread


from .threads import launch
from .utility import importer, md5sum, spl
from .workdir import moddir


NAME = inspect.getmodulename(__file__)


j = os.path.join
lock = threading.RLock()
path = os.path.dirname(inspect.getfile(importer))


class Mods:

    ignore = ""
    md5s = {}
    mods = [j(path, "modules"), j(path, "network"), "mods"]
    package = ".".join([NAME, "mdoules"])


def getmod(name, path=None):
    with lock:
        assert Mods.mods
        assert Mods.package
        mname = Mods.package + "." +  name
        module = sys.modules.get(mname, None)
        if module:
            return module
        mods = Mods.mods
        if path:
            mods.append(path)
        for path in mods:
            pth = os.path.join(path, f"{name}.py")
            if Mods.md5s and os.path.exists(pth) and name != "tbl":
                if md5sum(pth) != Mods.md5s.get(name, None):
                    logging.warning(
                                    "md5 error on %s",
                                    pth.split(os.sep)[-1]
                                   )
            mod = importer(mname, pth)
            if mod:
                return mod


def inits(names):
    modules = []
    for name in sorted(spl(names)):
        try:
            module = getmod(name)
            if not module:
                continue
            if "init" in dir(module):
                thr = launch(module.init)
                modules.append((module, thr))
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()
    return modules


def modules():
    modules = []
    for path in Mods.mods:
        modules.extend(list({
            x[:-3] for x in os.listdir(path)
            if x.endswith(".py") and not x.startswith("__") and
            x[:-3] not in spl(Mods.ignore)
           }))
    return sorted(modules)


def sums(checksum):
    assert Mods.mods
    table = getmod("tbl")
    if table:
        if "MD5" in dir(table):
            Mods.md5s.update(table.MD5)


def __dir__():
    return (
        'Mods',
        'getmod',
        'init',
        'modules',
        'sums'
    )
