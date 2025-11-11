# This file is placed in the Public Domain.


from tob.command import modules


def mod(event):
    event.reply(",".join(modules()))
