# This file is placed in the Public Domain.




from types import ModuleType

from .threads import Thread


class Kernel:

    @staticmethod
    def configure() -> None: ...


def scanner(
            names: list[str],
            init=False
           ) -> list[tuple[ModuleType, Thread]]: ...


def __dir__():
    return (
        'Kernel',
        'scanner'
    )
