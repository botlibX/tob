# This file is placed in the Public Domain.


"show modules"


def mod(event):
    from tob.command import modules
    event.reply(",".join(modules()))
