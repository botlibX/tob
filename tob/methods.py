# This file is placed in the Public Domain.


"object as the first argument"


import datetime
import os


from .objects import items, keys


def deleted(object):
    return "__deleted__" in dir(object) and object.__deleted__


def edit(object, setter, skip=True):
    for key, val in items(setter):
        if skip and val == "":
            continue
        try:
            setattr(object, key, int(val))
            continue
        except ValueError:
            pass
        try:
            setattr(object, key, float(val))
            continue
        except ValueError:
            pass
        if val in ["True", "true"]:
            setattr(object, key, True)
        elif val in ["False", "false"]:
            setattr(object, key, False)
        else:
            setattr(object, key, val)


def fmt(object, args=None, skip=None, plain=False, empty=False):
    if args is None:
        args = keys(object)
    if skip is None:
        skip = []
    text = ""
    for key in args:
        if key.startswith("__"):
            continue
        if key in skip:
            continue
        value = getattr(object, key, None)
        if value is None:
            continue
        if not empty and not value:
            continue
        if plain:
            text += f"{value} "
        elif isinstance(value, str):
            text += f'{key}="{value}" '
        else:
            text += f"{key}={value} "
    return text.strip()


def fqn(object):
    kin = str(type(object)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{object.__module__}.{object.__name__}"
    return kin


def ident(object):
    return os.path.join(fqn(object), *str(datetime.datetime.now()).split())


def name(object):
    typ = type(object)
    if "__builtins__" in dir(typ):
        return object.__name__
    if "__self__" in dir(object):
        return f"{object.__self__.__class__.__name__}.{object.__name__}"
    if "__class__" in dir(object) and "__name__" in dir(object):
        return f"{object.__class__.__name__}.{object.__name__}"
    if "__class__" in dir(object):
        return f"{object.__class__.__module__}.{object.__class__.__name__}"
    if "__name__" in dir(object):
        return f"{object.__class__.__name__}.{object.__name__}"
    return ""


def parse(object, text=""):
    if text == "":
        if "text" in dir(object):
            text = object.text
        else:
            text = ""
    args = []
    object.args   = getattr(object, "args", [])
    object.cmd    = getattr(object, "cmd", "")
    object.gets   = getattr(object, "gets", "")
    object.index  = getattr(object, "index", None)
    object.inits  = getattr(object, "inits", "")
    object.mod    = getattr(object, "mod", "")
    object.opts   = getattr(object, "opts", "")
    object.result = getattr(object, "result", "")
    object.sets   = getattr(object, "sets", {})
    object.silent = getattr(object, "silent", "")
    object.text    = text or getattr(object, "text", "")
    object.otext   = object.text or getattr(object, "otext", "")
    _nr = -1
    for spli in object.otext.split():
        if spli.startswith("-"):
            try:
                object.index = int(spli[1:])
            except ValueError:
                object.opts += spli[1:]
            continue
        if "-=" in spli:
            key, value = spli.split("-=", maxsplit=1)
            object.silent[key] = value
            object.gets[key] = value
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            object.gets[key] = value
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                if object.mod:
                    object.mod += f",{value}"
                else:
                    object.mod = value
                continue
            object.sets[key] = value
            continue
        _nr += 1
        if _nr == 0:
            object.cmd = spli
            continue
        args.append(spli)
    if args:
        object.args = args
        object.text  = object.cmd or ""
        object.rest = " ".join(object.args)
        object.text  = object.cmd + " " + object.rest
    else:
        object.text = object.cmd or ""


def search(object, selector, matching=False):
    res = False
    if not selector:
        return res
    for key, value in items(selector):
        val = getattr(object, key, None)
        if not val:
            continue
        if matching and value == val:
            res = True
        elif str(value).lower() in str(val).lower() or value == "match":
            res = True
        else:
            res = False
            break
    return res


def __dir__():
    return (
        'deleted',
        'edit',
        'fmt',
        'fqn',
        'ident',
        'name',
        'parse',
        'search'
    )


__all__ = __dir__()
