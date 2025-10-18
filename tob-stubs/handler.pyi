# This file is placed in the Public Domain.


"handle events"


from typing import Callable, Literal


class Event:

    def __init__(self) -> None:
        ...
    
    def ready(self) -> None:
        ...
    
    def reply(self, txt: str) -> None:
        ...
    
    def wait(self, timeout=float) -> None:
        ...
    

class Handler:

    def __init__(self) -> None:
        ...
    
    def callback(self, event) -> None:
        ...
    
    def loop(self) -> None:
        ...
    
    def poll(self) -> Event:
        ...
    
    def put(self, event: Event) -> None:
        ...
    
    def register(self, type: str, callback: Callable[[Event], None]) -> None:
        ...
    
    def start(self) -> None:
        ...
    
    def stop(self) -> None:
        ...
    


class Client(Handler):

    def __init__(self) -> None:
        ...
    
    def announce(self, txt: str) -> None:
        ...
    
    def display(self, event: Event) -> None:
        ...
    
    def dosay(self, channel: str, txt: str) -> None:
        ...
    
    def raw(self, txt: str) -> None:
        ...
    
    def say(self, channel: str, txt: str) -> None:
        ...
    

def __dir__() -> tuple[Literal['Client'], Literal['Event'], Literal['Handler']]:
    ...
