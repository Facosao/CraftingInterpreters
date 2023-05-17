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

        return self.primary()

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

    # ------------------------- STATEMENTS -------------------------

    def declaration(self) -> Stmt | None:
        try:
            if self.match([TT.VAR]):
                return self.var_declaration()

            return self.statement()
        except ParseError:
            self.synchonize()
            return None

    def statement(self) -> Stmt:
        if self.match([TT.PRINT]):
            return self.print_statement()
        if self.match([TT.LEFT_BRACE]):
            return stmt.Block(self.block())

        return self.expression_statement()

    def assignment(self) -> Expr:
        expression = self.equality()

        if self.match([TT.EQUAL]):
            equals: Token = self.previous()
            value: Expr = self.assignment()

            if isinstance(expression, expr.Variable):
                name: Token = expression.name
                return expr.Assign(name, value)

            error.token_error(equals, "Invalid assignment target.")

        return expression

    def print_statement(self) -> Stmt:
        value: Expr = self.expression()
        self.consume(TT.SEMICOLON, "Expect ';' after value.")
        return stmt.Print(value)

    def expression_statement(self) -> Stmt:
        expr: Expr = self.expression()
        self.consume(TT.SEMICOLON, "Expect ';' after expression.")
        return stmt.ExpressionStmt(expr)

    def var_declaration(self):
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
