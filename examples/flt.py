# This file is placed in the Public Domain.


from tob.brokers import objs
from tob.methods import fqn


def flt(event):
    clts = list(objs("announce"))
    if event.args:
        index = int(event.args[0])
        if index < len(clts):
            event.reply(str(clts[index]))
        else:
            event.reply("no matching client in fleet.")
        return
    event.reply(' | '.join([fqn(o).split(".")[-1] for o in clts]))
