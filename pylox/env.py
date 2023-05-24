from __future__ import annotations
import error
from token_class import Token


class Environment:
    def __init__(self, enclosing: Environment | None = None) -> None:
        self.values: dict[str, object] = {}
        self.enclosing: Environment | None = enclosing

    def define(self, name: str, value: object):
        self.values.update({name: value})

    def get(self, name: Token) -> object:
        value = self.values.get(name.lexeme)
        if value is not None:
            return value

        if self.enclosing is not None:
            return self.enclosing.get(name)

        error_str = "Undefined variable '" + name.lexeme + "'."
        raise error.runtime_error(name, error_str)

    def assign(self, name: Token, value: object) -> None:
        # test_value = self.values.get(name.lexeme)
        if name.lexeme in self.values:
            self.values.update({name.lexeme: value})
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        error_str = "Undefined variable '" + name.lexeme + "'."
        raise error.runtime_error(name, error_str)


globals = Environment()
instance = globals
