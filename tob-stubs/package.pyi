# This file is placed in the Public Domain.


import os
import types




class Mods:

    dirs: dict[str, str] = {}
    ignore = ""
    package = __spec__.parent or ""
    path = os.path.dirname(__spec__.loader.path) # type: ignore

    @staticmethod
    def add(name: str, path: str) -> None: ...

    @staticmethod
    def configure() -> None: ...

    @staticmethod
    def get(name: str) -> types.ModuleType | None: ...


def modules() -> list[str]: ...


def __dir__():
    return (
        'Mods',
        'modules'
    )
