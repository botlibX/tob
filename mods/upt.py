# This file is placed in the Public Domain.


import time


from tob.utility import Utils


STARTTIME = time.time()


def upt(event):
    event.reply(Utils.elapsed(time.time()-STARTTIME))
