# This file is placed in the Public Domain.


"clean namespace"


from typing import Any, ItemsView, Iterator, KeysView, Literal, ValuesView


class Object:

    def __contains__(self, key) -> bool:
        ...
    
    def __iter__(self) -> Iterator[str]:
        ...
    
    def __len__(self) -> int:
        ...
    
    def __str__(self) -> str:
        ...
    

def construct(obj, *args, **kwargs) -> None:
    ...

def items(obj)-> ItemsView[str, Any]:
    ...

def keys(obj) -> KeysView[Any]:
    ...

def update(obj, data, empty=...) -> None:
    ...

def values(obj) -> ValuesView[Any]:
    ...


def __dir__() -> tuple[Literal['Object'], Literal['construct'], Literal['items'], Literal['keys'], Literal['update'], Literal['values']]:
    ...
