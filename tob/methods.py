# This file is placed in the Public Domain.


"object as the first argument"


import datetime
import os


from .objects import items, keys


def deleted(obj):
    return "__deleted__" in dir(obj) and obj.__deleted__


def edit(obj, setter, skip=True):
    for key, val in items(setter):
        if skip and val == "":
            continue
        try:
            setattr(obj, key, int(val))
            continue
        except ValueError:
            pass
        try:
            setattr(obj, key, float(val))
            continue
        except ValueError:
            pass
        if val in ["True", "true"]:
            setattr(obj, key, True)
        elif val in ["False", "false"]:
            setattr(obj, key, False)
        else:
            setattr(obj, key, val)


def fmt(obj, args=None, skip=None, plain=False, empty=False):
    if args is None:
        args = keys(obj)
    if skip is None:
        skip = []
    text = ""
    for key in args:
        if key.startswith("__"):
            continue
        if key in skip:
            continue
        value = getattr(obj, key, None)
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


def fqn(obj):
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def ident(obj):
    return os.path.join(fqn(obj), *str(datetime.datetime.now()).split())


def name(obj):
    typ = type(obj)
    if "__builtins__" in dir(typ):
        return obj.__name__
    if "__self__" in dir(obj):
        return f"{obj.__self__.__class__.__name__}.{obj.__name__}"
    if "__class__" in dir(obj) and "__name__" in dir(obj):
        return f"{obj.__class__.__name__}.{obj.__name__}"
    if "__class__" in dir(obj):
        return f"{obj.__class__.__module__}.{obj.__class__.__name__}"
    if "__name__" in dir(obj):
        return f"{obj.__class__.__name__}.{obj.__name__}"
    return ""


def parse(obj, text=""):
    if text == "":
        if "text" in dir(obj):
            text = obj.text
        else:
            text = ""
    args = []
    obj.args = getattr(obj, "args", [])
    obj.command = getattr(obj, "command", "")
    obj.gets = getattr(obj, "gets", "")
    obj.index = getattr(obj, "index", None)
    obj.inits = getattr(obj, "inits", "")
    obj.mod = getattr(obj, "mod", "")
    obj.opts = getattr(obj, "opts", "")
    obj.result = getattr(obj, "result", "")
    obj.sets = getattr(obj, "sets", {})
    obj.silent = getattr(obj, "silent", "")
    obj.text = text or getattr(obj, "text", "")
    obj.otext = obj.text or getattr(obj, "otext", "")
    _nr = -1
    for spli in obj.otext.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "-=" in spli:
            key, value = spli.split("-=", maxsplit=1)
            obj.silent[key] = value
            obj.gets[key] = value
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            obj.gets[key] = value
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                if obj.mod:
                    obj.mod += f",{value}"
                else:
                    obj.mod = value
                continue
            obj.sets[key] = value
            continue
        _nr += 1
        if _nr == 0:
            obj.command = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.text  = obj.command or ""
        obj.rest = " ".join(obj.args)
        obj.text  = obj.command + " " + obj.rest
    else:
        obj.text = obj.command or ""


def search(obj, selector, matching=False):
    res = False
    if not selector:
        return res
    for key, value in items(selector):
        val = getattr(obj, key, None)
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
