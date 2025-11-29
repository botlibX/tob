# This file is placed in the Public Domain.


import logging


from .statics import LEVELS


class Logging:

    datefmt = "%H:%M:%S"
    format = "%(module).3s %(message)s"


class Format(logging.Formatter):

    def format(self, record):
        record.module = record.module.upper()
        return logging.Formatter.format(self, record)


def level(loglevel: str ="debug") -> None: ...


def __dir__():
    return (
        'Logging',
        'level'
    )
