# This file is placed in the Public Domain.


from tob.brokers import all
from tob.methods import fmt
from tob.threads import name


def flt(event):
    if event.args:
        clts = all("announce")
        index = int(event.args[0])
        if index < len(clts):
            event.reply(fmt(list(all())[index], empty=True))
        else:
            event.reply(f"only {len(clts)} clients in fleet.")
        return
    event.reply(' | '.join([name(o) for o in all()]))
