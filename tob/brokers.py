# This file is placed in the Public Domain.


"an object for a string"


class Fleet:

    clients = {}

    @staticmethod
    def add(client):
        if not client:
            return
        Fleet.clients[repr(client)] = client

    @staticmethod
    def all():
        return list(Fleet.clients.values())

    @staticmethod
    def announce(txt):
        for client in Fleet.all():
            client.announce(txt)

    @staticmethod
    def display(event):
        client = Fleet.get(event.origin)
        client.display(event)

    @staticmethod
    def get(origin):
        return Fleet.clients.get(origin, None)

    @staticmethod
    def say(origin, channel, txt):
        client = Fleet.get(origin)
        client.say(channel, txt)

    @staticmethod
    def shutdown():
        for client in Fleet.all():
            client.stop()
            client.wait()


def __dir__():
    return (
        'Fleet',
   )
