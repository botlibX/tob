# This file is placed in the Public Domain.


import time


from tob.utility import elapsed


STARTTIME = time.time()


def upt(event):
    event.reply(elapsed(time.time()-STARTTIME))
