# This file is placed in the Public Domain.


"json serializer"


from json import JSONEncoder, load, loads
from typing import Any, Iterator, Literal, ValuesView


class Encoder(JSONEncoder):

    def default(self, o) -> ValuesView[Any] | Iterator[Any] | Any | str:
        ...
    

def dump(obj, fp, *args, **kw) -> None:
    ...

def dumps(obj, *args, **kw) -> str:
    ...

def __dir__() -> tuple[Literal['dump'], Literal['dumps'], Literal['load'], Literal['loads']]:
    ...
