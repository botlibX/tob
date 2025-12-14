# This file is placed in the Public Domain.


from tob.pkg import Mods


def mod(event):
    event.reply(Mods.list())
