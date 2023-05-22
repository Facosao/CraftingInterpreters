from __future__ import annotations
from token_type import TokenType
from token_class import Token
from expr import Expr
import expr
import stmt
from stmt import Stmt
import token_type_instances as TT
import error


class ParseError(Exception):
    ...


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens
        self.current: int = 0

    def parse(self) -> list[Stmt]:
        statements: list[Stmt] = []
        while not self.is_at_end():
            stmt = self.declaration()
            if isinstance(stmt, Stmt):
                statements.append(stmt)

        return statements

    def match(self, types: list[TokenType]) -> bool:
        for lox_type in types:
            if self.check(lox_type):
                self.advance()
                return True

        return False

    def consume(self, lox_type: TokenType, message: str) -> Token:
        if self.check(lox_type):
            return self.advance()

        raise self.error(self.peek(), message)

    def error(self, lox_token: Token, message: str) -> ParseError:
        error.token_error(lox_token, message)
        return ParseError()

    def synchonize(self) -> None:
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TT.SEMICOLON:
                return

            match self.peek().type.value:
                case TT.CLASS.value | TT.FUN.value | TT.RETURN.value:
                    return
                case TT.WHILE.value | TT.FOR.value | TT.IF.value:
                    return
                case TT.PRINT.value | TT.VAR.value:
                    return

            self.advance()

    def check(self, arg_type: TokenType) -> bool:
        if self.is_at_end():
            return False

        return self.peek().type == arg_type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1

        return self.previous()

    def is_at_end(self):
        return self.peek().type == TT.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    # ------------------------- EXPRESSIONS -------------------------

    def expression(self):
        return self.assignment()

    def assignment(self) -> Expr:
        expression = self.logical_or()

        if self.match([TT.EQUAL]):
            equals: Token = self.previous()
            value: Expr = self.assignment()

            if isinstance(expression, expr.Variable):
                name: Token = expression.name
                return expr.Assign(name, value)

            error.token_error(equals, "Invalid assignment target.")

        return expression

    def logical_or(self) -> Expr:
        expression: Expr = self.logical_and()

        while self.match([TT.OR]):
            operator: Token = self.previous()
            right: Expr = self.logical_and()
            expression = expr.Logical(expression, operator, right)

        return expression

    def logical_and(self) -> Expr:
        expression: Expr = self.equality()

        while self.match([TT.AND]):
            operator: Token = self.previous()
            right: Expr = self.equality()
            expression = expr.Logical(expression, operator, right)

        return expression

    def equality(self):
        new_expr = self.comparison()

        while self.match([TT.BANG_EQUAL, TT.EQUAL_EQUAL]):
            operator: Token = self.previous()
            right: Expr = self.comparison()
            new_expr = expr.Binary(new_expr, operator, right)

        return new_expr

    def comparison(self) -> Expr:
        new_expr = self.term()

        while self.match(
            [
                TT.GREATER,
                TT.GREATER_EQUAL,
                TT.LESS,
                TT.LESS_EQUAL,
            ]
        ):
            operator: Token = self.previous()
            right: Expr = self.term()
            new_expr = expr.Binary(new_expr, operator, right)

        return new_expr

    def term(self) -> Expr:
        new_expr = self.factor()

        while self.match([TT.MINUS, TT.PLUS]):
            operator: Token = self.previous()
            right: Expr = self.factor()
            new_expr = expr.Binary(new_expr, operator, right)

        return new_expr

    def factor(self) -> Expr:
        new_expr = self.unary()

        while self.match([TT.SLASH, TT.STAR]):
            operator: Token = self.previous()
            right: Expr = self.unary()
            new_expr = expr.Binary(new_expr, operator, right)

        return new_expr

    def unary(self) -> Expr:
        if self.match([TT.BANG, TT.MINUS]):
            operator: Token = self.previous()
            right: Expr = self.unary()
            return expr.Unary(operator, right)

        return self.call()

    def primary(self) -> Expr:
        if self.match([TT.FALSE]):
            return expr.Literal(False)

        if self.match([TT.TRUE]):
            return expr.Literal(True)

        if self.match([TT.NIL]):
            return expr.Literal(None)

        if self.match([TT.NUMBER, TT.STRING]):
            return expr.Literal(self.previous().literal)

        if self.match([TT.IDENTIFIER]):
            return expr.Variable(self.previous())

        if self.match([TT.LEFT_PAREN]):
            new_expr = self.expression()
            self.consume(TT.RIGHT_PAREN, "Expect ')' after expression.")
            return expr.Grouping(new_expr)

        raise self.error(self.peek(), "Expect expression.")

    def call(self) -> Expr:
        expression: Expr = self.primary()

        while True:
            if self.match([TT.LEFT_PAREN]):
                expression = self.finish_call(expression)
            else:
                break

        return expression

    def finish_call(self, callee: Expr) -> Expr:
        args: list[Expr] = []

        if not self.check(TT.RIGHT_PAREN):
            args.append(self.expression())
            while self.match([TT.COMMA]):
                if len(args) >= 255:
                    # This raises an exception -> divergence from book?
                    self.error(self.peek(), "Can't have more than 255 arguments.")

                args.append(self.expression())

        paren: Token = self.consume(TT.RIGHT_PAREN, "Expect ')' after arguments.")

        return expr.Call(callee, paren, args)

    # ------------------------- STATEMENTS -------------------------

    def statement(self) -> Stmt:
        if self.match([TT.IF]):
            return self.if_statement()
        if self.match([TT.PRINT]):
            return self.print_statement()
        if self.match([TT.WHILE]):
            return self.while_statement()
        if self.match([TT.FOR]):
            return self.for_statement()
        if self.match([TT.LEFT_BRACE]):
            return stmt.Block(self.block())

        return self.expression_statement()

    def declaration(self) -> Stmt | None:
        try:
            if self.match([TT.FUN]):
                return self.function("function")
            if self.match([TT.VAR]):
                return self.var_declaration()

            return self.statement()
        except ParseError:
            self.synchonize()
            return None

    def print_statement(self) -> stmt.Print:
        value: Expr = self.expression()
        self.consume(TT.SEMICOLON, "Expect ';' after value.")
        return stmt.Print(value)

    def expression_statement(self) -> stmt.ExpressionStmt:
        expr: Expr = self.expression()
        self.consume(TT.SEMICOLON, "Expect ';' after expression.")
        return stmt.ExpressionStmt(expr)

    def var_declaration(self) -> stmt.Var:
        name: Token = self.consume(TT.IDENTIFIER, "Expect variable name.")

        initializer: Expr | None = None
        if self.match([TT.EQUAL]):
            initializer = self.expression()

        self.consume(TT.SEMICOLON, "Expect ';' after variable declaration.")
        return stmt.Var(name, initializer)

    def block(self) -> list[Stmt]:
        statements: list[Stmt] = []

        while (not self.check(TT.RIGHT_BRACE)) and (not self.is_at_end()):
            decl = self.declaration()
            if decl is not None:
                statements.append(decl)

        self.consume(TT.RIGHT_BRACE, "Expect } after block.")
        return statements

    def if_statement(self) -> stmt.If:
        self.consume(TT.LEFT_PAREN, "Expect '(' after 'if'.")
        condition: Expr = self.expression()
        self.consume(TT.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch: Stmt = self.statement()
        else_branch: Stmt | None = None
        if self.match([TT.ELSE]):
            else_branch = self.statement()

        return stmt.If(condition, then_branch, else_branch)

    def while_statement(self) -> stmt.While:
        self.consume(TT.LEFT_PAREN, "Expect '(' after 'while'.")
        condition: Expr = self.expression()
        self.consume(TT.RIGHT_PAREN, "Expect ')' after condition.")
        body: Stmt = self.statement()

        return stmt.While(condition, body)

    def for_statement(self) -> Stmt:
        self.consume(TT.LEFT_PAREN, "Expect '(' after 'for'.")

        if self.match([TT.SEMICOLON]):
            initializer: Stmt | None = None
        elif self.match([TT.VAR]):
            initializer: Stmt | None = self.var_declaration()
        else:
            initializer: Stmt | None = self.expression_statement()

        condition: Expr | None = None
        if not self.check(TT.SEMICOLON):
            condition = self.expression()
        self.consume(TT.SEMICOLON, "Expect ';' after loop condition.")

        increment: Expr | None = None
        if not self.check(TT.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TT.RIGHT_PAREN, "Expect ')' after for clauses.")

        body: Stmt = self.statement()

        if increment is not None:
            body = stmt.Block([body, stmt.ExpressionStmt(increment)])

        if condition is None:
            condition = expr.Literal(True)
        body = stmt.While(condition, body)

        if initializer is not None:
            body = stmt.Block([initializer, body])

        return body

    def function(self, kind: str) -> stmt.Function:
        name: Token = self.consume(TT.IDENTIFIER, "Expect " + kind + " name.")
        params: list[Token] = []

        if not self.check(TT.RIGHT_PAREN):
            params.append(self.consume(TT.IDENTIFIER, "Expect parameter name."))
            while self.match([TT.COMMA]):
                if len(params) >= 255:
                    # Same concern as self.finish_call()
                    self.error(self.peek(), "Can't have more than 255 arguments.")

                params.append(self.consume(TT.IDENTIFIER, "Expect parameter name."))

        self.consume(TT.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TT.LEFT_BRACE, "Expect '{' before " + kind + " body.")
        body: list[Stmt] = self.block()

        return stmt.Function(name, params, body)
