from token_type import TokenType
from token_class import Token
from expr import Expr
import expr
import token_type_instances as TT
import error


class ParseError(Exception):
    ...


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens
        self.current: int = 0

    def parse(self) -> Expr | None:
        try:
            return self.__expression()
        except ParseError:
            return None

    def __match(self, types: list[TokenType]) -> bool:
        for lox_type in types:
            if self.__check(lox_type):
                self.__advance()
                return True

        return False

    def __consume(self, lox_type: TokenType, message: str) -> Token:
        if self.__check(lox_type):
            return self.__advance()

        raise self.__error(self.__peek(), message)

    def __error(self, lox_token: Token, message: str) -> ParseError:
        error.token_error(lox_token, message)
        return ParseError()

    def __synchonize(self) -> None:
        self.__advance()

        while not self.__is_at_end():
            if self.__previous().type == TT.SEMICOLON:
                return

            match self.__peek().type.value:
                case TT.CLASS.value | TT.FUN.value | TT.VAR.value:
                    return
                case TT.FOR.value | TT.IF.value | TT.WHILE.value:
                    return
                case TT.PRINT.value | TT.RETURN.value:
                    return

            self.__advance()

    def __check(self, arg_type: TokenType) -> bool:
        if self.__is_at_end():
            return False

        return self.__peek().type == arg_type

    def __advance(self) -> Token:
        if not self.__is_at_end():
            self.current += 1

        return self.__previous()

    def __is_at_end(self):
        return self.__peek().type == TT.EOF

    def __peek(self) -> Token:
        return self.tokens[self.current]

    def __previous(self) -> Token:
        return self.tokens[self.current - 1]

    def __expression(self):
        return self.__equality()

    def __equality(self):
        new_expr = self.__comparison()

        while self.__match([TT.BANG_EQUAL, TT.EQUAL_EQUAL]):
            operator: Token = self.__previous()
            right: Expr = self.__comparison()
            new_expr = expr.Binary(new_expr, operator, right)

        return new_expr

    def __comparison(self) -> Expr:
        new_expr = self.__term()

        while self.__match(
            [
                TT.GREATER,
                TT.GREATER_EQUAL,
                TT.LESS,
                TT.LESS_EQUAL,
            ]
        ):
            operator: Token = self.__previous()
            right: Expr = self.__term()
            new_expr = expr.Binary(new_expr, operator, right)

        return new_expr

    def __term(self) -> Expr:
        new_expr = self.__factor()

        while self.__match([TT.MINUS, TT.PLUS]):
            operator: Token = self.__previous()
            right: Expr = self.__factor()
            new_expr = expr.Binary(new_expr, operator, right)

        return new_expr

    def __factor(self) -> Expr:
        new_expr = self.__unary()

        while self.__match([TT.SLASH, TT.STAR]):
            operator: Token = self.__previous()
            right: Expr = self.__unary()
            new_expr = expr.Binary(new_expr, operator, right)

        return new_expr

    def __unary(self) -> Expr:
        if self.__match([TT.BANG, TT.MINUS]):
            operator: Token = self.__previous()
            right: Expr = self.__unary()
            return expr.Unary(operator, right)

        return self.__primary()

    def __primary(self) -> Expr:
        if self.__match([TT.FALSE]):
            return expr.Literal(False)

        if self.__match([TT.TRUE]):
            return expr.Literal(True)

        if self.__match([TT.NIL]):
            return expr.Literal(None)

        if self.__match([TT.NUMBER, TT.STRING]):
            return expr.Literal(self.__previous().literal)

        if self.__match([TT.LEFT_PAREN]):
            new_expr = self.__expression()
            self.__consume(TT.RIGHT_PAREN, "Expect ')' after expression.")
            return expr.Grouping(new_expr)

        raise self.__error(self.__peek(), "Expect expression.")
