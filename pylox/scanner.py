from token_class import Token
from token_type import TokenType
import lox as Lox


class Scanner:
    def __init__(self, source: str) -> None:
        self.source: str = source
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def scan_tokens(self) -> list[Token]:
        while not self.__is_at_end():
            self.start = self.current
            break

        self.tokens.append(Token(TokenType(TokenType.EOF), "", None, self.line))
        return self.tokens

    def __is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def __advance(self) -> str:
        character = self.source[self.current]
        self.current += 1
        return character

    def __add_token(self, type: TokenType, literal: object = "PyLoxNULL") -> None:
        text: str = self.source[self.start : self.current]  # Check for correctness
        self.tokens.append(Token(type, text, literal, self.line))

    def __scan_token(self) -> None:
        character = self.__advance()

        match character:
            case "(":
                self.__add_token(TokenType(TokenType.LEFT_PAREN))
            case ")":
                self.__add_token(TokenType(TokenType.RIGHT_BRACE))
            case "{":
                self.__add_token(TokenType(TokenType.LEFT_BRACE))
            case "}":
                self.__add_token(TokenType(TokenType.RIGHT_BRACE))
            case ",":
                self.__add_token(TokenType(TokenType.COMMA))
            case ".":
                self.__add_token(TokenType(TokenType.DOT))
            case "-":
                self.__add_token(TokenType(TokenType.MINUS))
            case "+":
                self.__add_token(TokenType(TokenType.PLUS))
            case ";":
                self.__add_token(TokenType(TokenType.SEMICOLON))
            case "*":
                self.__add_token(TokenType(TokenType.STAR))
            case _:
                Lox.error(self.line, "Unexpected character.")
