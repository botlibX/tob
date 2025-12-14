# This file is placed in the Public Domain.


import os


from tob.pkg import Mods


def pth(event):
    path = os.path.join(Mods.path, 'network', 'html', "index.html")
    event.reply(f"file://{path}")
