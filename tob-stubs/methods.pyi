# This file is placed in the Poblic Domain.


"object as the first argument"


from typing import Any, Literal


def deleted(obj) -> Literal[False]:
    ...

def edit(obj, setter, skip=...) -> None:
    ...

def fmt(obj, args=..., skip=..., plain=..., empty=...) -> str:
    ...

def name(obj, short=...) -> str:
    ...

def parse(obj, txt=...) -> None:
    ...

def search(obj, selector, matching=...) -> bool:
    ...


def __dir__()  -> tuple[Literal['deleted'], Literal['edit'], Literal['fmt'], Literal['parse'], Literal['search']]:
    ...
