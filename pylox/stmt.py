import error
import expr
import env
from expr import Expr
from token_class import Token


class Stmt:
    def __init__(self) -> None:
        raise error.AbstractClassInstance

    def interpret(self) -> None:
        raise error.UndefinedMethod


class ExpressionStmt(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression: Expr = expression

    def interpret(self) -> None:
        self.expression.interpret()


class Print(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression: Expr = expression

    def interpret(self) -> None:
        value: object = self.expression.interpret()
        print(expr.stringify(value))


class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr | None) -> None:
        self.name: Token = name
        self.initializer: Expr | None = initializer

    def interpret(self) -> None:
        value = None
        if isinstance(self.initializer, Expr):
            value = self.initializer.interpret()

        env.instance.define(self.name.lexeme, value)


class Block(Stmt):
    def __init__(self, statements: list[Stmt]) -> None:
        self.statements = statements

    def interpret(self) -> None:
        execute_block(self.statements, env.Environment(env.instance))


def execute_block(statements: list[Stmt], environment: env.Environment):
    previous: env.Environment = env.instance
    try:
        env.instance = environment

        for statement in statements:
            statement.interpret()
    finally:
        env.instance = previous
