# This file is placed in the Public Domain.


import time


from ..utility import STARTTIME, elapsed


def upt(event):
    event.reply(elapsed(time.time()-STARTTIME))
