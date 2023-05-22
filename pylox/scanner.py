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
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TT.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        character = self.source[self.current]
        self.current += 1
        return character

    def add_token(self, type: TokenType, literal: object = None) -> None:  # PyLoxNULL
        text: str = self.source[self.start : self.current]  # Check for correctness
        self.tokens.append(Token(type, text, literal, self.line))

    def scan_token(self) -> None:
        character = self.advance()

        match character:
            case "(":
                self.add_token(TT.LEFT_PAREN)
            case ")":
                self.add_token(TT.RIGHT_PAREN)
            case "{":
                self.add_token(TT.LEFT_BRACE)
            case "}":
                self.add_token(TT.RIGHT_BRACE)
            case ",":
                self.add_token(TT.COMMA)
            case ".":
                self.add_token(TT.DOT)
            case "-":
                self.add_token(TT.MINUS)
            case "+":
                self.add_token(TT.PLUS)
            case ";":
                self.add_token(TT.SEMICOLON)
            case "*":
                self.add_token(TT.STAR)
            case "!":
                token = TT.BANG_EQUAL if self.match("=") else TT.BANG
                self.add_token(token)
            case "=":
                token = TT.EQUAL_EQUAL if self.match("=") else TT.EQUAL
                self.add_token(token)
            case "<":
                token = TT.LESS_EQUAL if self.match("=") else TT.LESS
                self.add_token(token)
            case ">":
                token = TT.GREATER_EQUAL if self.match("=") else TT.GREATER
                self.add_token(token)
            case "/":
                if self.match("/"):
                    while (self.peek() != "\n") and (not self.is_at_end()):
                        self.advance()
                else:
                    self.add_token(TT.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case _:
                if self.is_digit(character):
                    self.number()
                elif self.is_alpha(character):
                    self.identifier()
                else:
                    error.line_error(self.line, "Unexpected character.")

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False

        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"

        return self.source[self.current]

    def string(self) -> None:
        while (self.peek() != '"') and (not self.is_at_end()):
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            error.line_error(self.line, "Unterminated string.")
            return

        self.advance()

        substr: str = self.source[self.start + 1 : self.current - 1]
        self.add_token(TT.STRING, substr)

    def is_digit(self, c: str) -> bool:
        return "0" <= c <= "9"

    def number(self) -> None:
        while self.is_digit(self.peek()):
            self.advance()

        if (self.peek() == ".") and (self.is_digit(self.peek_next())):
            # Consume the "."
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        new_number = float(self.source[self.start : self.current])
        self.add_token(TT.NUMBER, new_number)

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"

        return self.source[self.current + 1]

    def is_alpha(self, c: str) -> bool:
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or (c == "_")

    def is_alphanumeric(self, c: str) -> bool:
        return self.is_alpha(c) or self.is_digit(c)

    def identifier(self) -> None:
        while self.is_alphanumeric(self.peek()):
            self.advance()

        text: str = self.source[self.start : self.current]
        word: None | TokenType = self.keywords.get(text)
        if word == None:
            self.add_token(TT.IDENTIFIER)
        else:
            self.add_token(word)
