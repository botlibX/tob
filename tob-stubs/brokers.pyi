# This file is placed in the Public Domain.


"client for a string"


from typing import ValuesView


from tob.handler import Client, Event


class Fleet:

    clients: dict[str, Client]

    @staticmethod
    def add(client: Client) -> None:
        ...

    @staticmethod
    def all() -> ValuesView[Client]:
        ...
    
    @staticmethod
    def announce(txt: str) -> None:
        ...
    
    @staticmethod
    def display(evt: Event) -> None:
        ...
    
    @staticmethod
    def get(orig: str) -> Client:
        ...
    
    @staticmethod
    def say(orig: str, channel: str, txt: str) -> None:
        ...
    
    @staticmethod
    def shutdown() -> None:
        ...
    

def __dir__(): # -> tuple[Literal['Fleet']]:
    ...
