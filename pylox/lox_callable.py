import time


class LoxCallable:
    def __init__(self) -> None:
        raise NotImplementedError

    def call(self, arguments: list[object]) -> object:
        raise NotImplementedError

    def arity(self) -> int:
        raise NotImplementedError


class Clock(LoxCallable):
    def __init__(self) -> None:
        pass

    def call(self, arguments: list[object]) -> object:
        # Verify that this uses seconds as its measurement unit
        return time.perf_counter()

    def arity(self) -> int:
        return 0

    def __str__(self) -> str:
        return "<native fn>"
