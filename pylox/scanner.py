import error
from token_class import Token
from token_type import TokenType
import token_type_instances as TT


class Scanner:
    keywords: dict[str, TokenType] = {
        "and": TT.AND,
        "class": TT.CLASS,
        "else": TT.ELSE,
        "false": TT.FALSE,
        "for": TT.FOR,
        "fun": TT.FUN,
        "if": TT.IF,
        "nil": TT.NIL,
        "or": TT.OR,
        "print": TT.PRINT,
        "return": TT.RETURN,
        "super": TT.SUPER,
        "this": TT.THIS,
        "true": TT.TRUE,
        "var": TT.VAR,
        "while": TT.WHILE,
    }

    def __init__(self, source: str) -> None:
        self.source: str = source
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def scan_tokens(self) -> list[Token]:
        while not self.__is_at_end():
            self.start = self.current
            self.__scan_token()

        self.tokens.append(Token(TT.EOF, "", None, self.line))
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
                self.__add_token(TT.LEFT_PAREN)
            case ")":
                self.__add_token(TT.RIGHT_PAREN)
            case "{":
                self.__add_token(TT.LEFT_BRACE)
            case "}":
                self.__add_token(TT.RIGHT_BRACE)
            case ",":
                self.__add_token(TT.COMMA)
            case ".":
                self.__add_token(TT.DOT)
            case "-":
                self.__add_token(TT.MINUS)
            case "+":
                self.__add_token(TT.PLUS)
            case ";":
                self.__add_token(TT.SEMICOLON)
            case "*":
                self.__add_token(TT.STAR)
            case "!":
                token = TT.BANG_EQUAL if self.__match("=") else TT.BANG
                self.__add_token(token)
            case "=":
                token = TT.EQUAL_EQUAL if self.__match("=") else TT.EQUAL
                self.__add_token(token)
            case "<":
                token = TT.LESS_EQUAL if self.__match("=") else TT.LESS
                self.__add_token(token)
            case ">":
                token = TT.GREATER_EQUAL if self.__match("=") else TT.GREATER
                self.__add_token(token)
            case "/":
                if self.__match("/"):
                    while (self.__peek() != "\n") and (not self.__is_at_end()):
                        self.__advance()
                else:
                    self.__add_token(TT.SLASH)
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
                    error.error(self.line, "Unexpected character.")

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
            error.error(self.line, "Unterminated string.")
            return

        self.__advance()

        substr: str = self.source[self.start + 1 : self.current - 1]
        self.__add_token(TT.STRING, substr)

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
        self.__add_token(TT.NUMBER, new_number)

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
            self.__add_token(TT.IDENTIFIER)
        else:
            self.__add_token(word)
