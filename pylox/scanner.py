import error
from token_class import Token
from token_type import TokenType


class Scanner:
    keywords: dict[str, TokenType] = {
        "and": TokenType(TokenType.AND),
        "class": TokenType(TokenType.CLASS),
        "else": TokenType(TokenType.ELSE),
        "false": TokenType(TokenType.FALSE),
        "for": TokenType(TokenType.FOR),
        "fun": TokenType(TokenType.FUN),
        "if": TokenType(TokenType.IF),
        "nil": TokenType(TokenType.NIL),
        "or": TokenType(TokenType.OR),
        "print": TokenType(TokenType.PRINT),
        "return": TokenType(TokenType.RETURN),
        "super": TokenType(TokenType.SUPER),
        "this": TokenType(TokenType.THIS),
        "true": TokenType(TokenType.TRUE),
        "var": TokenType(TokenType.VAR),
        "while": TokenType(TokenType.WHILE),
    }

    def __init__(self, source: str, error_var: bool) -> None:
        self.source: str = source
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1
        self.had_error: bool = error_var

    def scan_tokens(self) -> list[Token]:
        while not self.__is_at_end():
            self.start = self.current
            self.__scan_token()

        self.tokens.append(Token(TokenType(TokenType.EOF), "", None, self.line))
        return self.tokens

    def __is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def __advance(self) -> str:
        character = self.source[self.current]
        self.current += 1
        return character

    def __add_token(self, type: TokenType, literal: object = None) -> None:  # PyLoxNULL
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
            case "!":
                token = (
                    TokenType(TokenType.BANG_EQUAL)
                    if self.__match("=")
                    else TokenType(TokenType.BANG)
                )
                self.__add_token(token)
            case "=":
                token = (
                    TokenType(TokenType.EQUAL_EQUAL)
                    if self.__match("=")
                    else TokenType(TokenType.EQUAL)
                )
                self.__add_token(token)
            case "<":
                token = (
                    TokenType(TokenType.LESS_EQUAL)
                    if self.__match("=")
                    else TokenType(TokenType.LESS)
                )
                self.__add_token(token)
            case ">":
                token = (
                    TokenType(TokenType.GREATER_EQUAL)
                    if self.__match("=")
                    else TokenType(TokenType.GREATER)
                )
                self.__add_token(token)
            case "/":
                if self.__match("/"):
                    while (self.__peek() != "\n") and (not self.__is_at_end()):
                        self.__advance()
                else:
                    self.__add_token(TokenType(TokenType.SLASH))
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case '"':
                self.__string()
            case _:
                if self.__is_digit(character):
                    self.__number()
                elif self.__is_alpha(character):
                    self.__identifier()
                else:
                    error.error(self.line, "Unexpected character.", self.had_error)

    def __match(self, expected: str) -> bool:
        if self.__is_at_end():
            return False

        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def __peek(self) -> str:
        if self.__is_at_end():
            return "\0"

        return self.source[self.current]

    def __string(self) -> None:
        while (self.__peek() != '"') and (not self.__is_at_end()):
            if self.__peek() == "\n":
                self.line += 1
            self.__advance()

        if self.__is_at_end():
            error.error(self.line, "Unterminated string.", self.had_error)
            return

        self.__advance()

        substr: str = self.source[self.start + 1 : self.current - 1]
        self.__add_token(TokenType(TokenType.STRING), substr)

    def __is_digit(self, c: str) -> bool:
        return "0" <= c <= "9"

    def __number(self) -> None:
        while self.__is_digit(self.__peek()):
            self.__advance()

        if (self.__peek() == ".") and (self.__is_digit(self.__peek_next())):
            # Consume the "."
            self.__advance()

            while self.__is_digit(self.__peek()):
                self.__advance()

        new_number = float(self.source[self.start : self.current])
        self.__add_token(TokenType(TokenType.NUMBER), new_number)

    def __peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"

        return self.source[self.current + 1]

    def __is_alpha(self, c: str) -> bool:
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or (c == "_")

    def __is_alphanumeric(self, c: str) -> bool:
        return self.__is_alpha(c) or self.__is_digit(c)

    def __identifier(self) -> None:
        while self.__is_alphanumeric(self.__peek()):
            self.__advance()

        text: str = self.source[self.start : self.current]
        word: None | TokenType = self.keywords.get(text)
        if word == None:
            self.__add_token(TokenType(TokenType.IDENTIFIER))
        else:
            self.__add_token(word)
