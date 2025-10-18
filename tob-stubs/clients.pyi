# This file is placed in the Public Domain.


"client events"


from typing import Any, Literal


from tob.handler import Client


class Output(Client):

    def output(self) -> None:
        ...
    
    def start(self) -> None:
        ...
    
    def stop(self) -> None:
        ...
    
    def wait(self) -> None:
        ...
    

def __dir__() -> Literal['Output']:
    ...
