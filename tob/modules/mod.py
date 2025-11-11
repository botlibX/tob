# This file is placed in the Public Domain.


from ..command import modules


def mod(event):
    event.reply(",".join(modules()))
