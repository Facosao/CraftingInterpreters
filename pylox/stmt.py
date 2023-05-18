import error
import expr
import env
from expr import Expr
from token_class import Token


class Stmt:
    def __init__(self) -> None:
        raise NotImplementedError

    def interpret(self) -> None:
        raise NotImplementedError


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


class If(Stmt):
    def __init__(
        self, condition: Expr, then_branch: Stmt, else_branch: Stmt | None
    ) -> None:
        self.condition: Expr = condition
        self.then_branch: Stmt = then_branch
        self.else_branch: Stmt | None = else_branch

    def interpret(self) -> None:
        if expr.is_truthy(self.condition.interpret()):
            self.then_branch.interpret()
        elif self.else_branch is not None:
            self.else_branch.interpret()


class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt) -> None:
        self.condition: Expr = condition
        self.body: Stmt = body

    def interpret(self) -> None:
        while expr.is_truthy(self.condition.interpret()):
            self.body.interpret()


def execute_block(statements: list[Stmt], environment: env.Environment):
    previous: env.Environment = env.instance
    try:
        env.instance = environment

        for statement in statements:
            statement.interpret()
    finally:
        env.instance = previous
