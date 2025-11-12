# This file is placed in the Public Domain.


import inspect


from typing import Callable


from .objects import Default, Object, values


class Commands:

    cmds: dict[str, Callable] = {}
    names: dict[str, str] = {}

    @staticmethod
    def add(*args):
        for func in args:
            name = func.__name__
            Commands.cmds[name] = func
            Commands.names[name] = func.__module__.split(".")[-1]

    @staticmethod
    def get(cmd):
        return Commands.cmds.get(cmd, None)


class Fleet:

    clients = Object()

    @staticmethod
    def add(client):
        setattr(Fleet.clients, repr(client), client)

    @staticmethod
    def all():
        return values(Fleet.clients)

    @staticmethod
    def announce(text):
        for client in Fleet.all():
            client.announce(text)

    @staticmethod
    def display(event):
        client = Fleet.get(event.orig)
        if client:
            client.display(event)

    @staticmethod
    def get(origin):
        return getattr(Fleet.clients, origin, None)

    @staticmethod
    def like(origin):
        for orig in Fleet.clients:
            if origin.split()[0] in orig.split()[0]:
                yield orig

    @staticmethod
    def say(orig, channel, txt):
        client = Fleet.get(orig)
        if client:
            client.say(channel, txt)

    @staticmethod
    def shutdown():
        for client in Fleet.all():
            client.wait()
            client.stop()



def command(evt):
    parse(evt, evt.text)
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        Fleet.display(evt)
    evt.ready()


def scan(module):
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in inspect.signature(cmdz).parameters:
            Commands.add(cmdz)


def parse(obj, text) -> None:
    data = {
        "args": [],
        "cmd": "",
        "gets": Default(),
        "index": None,
        "init": "",
        "opts": "",
        "otxt": text,
        "rest": "",
        "silent": Default(),
        "sets": Default(),
        "text": text
    }
    for k, v in data.items():
        setattr(obj, k, getattr(obj, k, v) or v)
    args = []
    nr = -1
    for spli in text.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "-=" in spli:
            key, value = spli.split("-=", maxsplit=1)
            setattr(obj.silent, key, value)
            setattr(obj.gets, key, value)
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            setattr(obj.gets, key, value)
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            setattr(obj.sets, key, value)
            continue
        nr += 1
        if nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.text  = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.text  = obj.cmd + " " + obj.rest
    else:
        obj.text = obj.cmd or ""


def __dir__():
    return (
        'Comamnds',
        'Mods',
        'command',
        'importer',
        'modules',
        'scan',
        'scanner'
    )
