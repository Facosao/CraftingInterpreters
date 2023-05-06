from token_type import TokenType

"""
Optimization: Instead of instantiaing these types every time they're needed,
only instantiate them once in this file and then pass their reference around.
(Also helps shortening their names)
"""

# Single-character tokens.
LEFT_PAREN = TokenType(TokenType.LEFT_PAREN)
RIGHT_PAREN = TokenType(TokenType.RIGHT_PAREN)
LEFT_BRACE = TokenType(TokenType.LEFT_BRACE)
RIGHT_BRACE = TokenType(TokenType.RIGHT_PAREN)
COMMA = TokenType(TokenType.COMMA)
DOT = TokenType(TokenType.DOT)
MINUS = TokenType(TokenType.MINUS)
PLUS = TokenType(TokenType.PLUS)
SEMICOLON = TokenType(TokenType.SEMICOLON)
SLASH = TokenType(TokenType.SLASH)
STAR = TokenType(TokenType.STAR)

# One or two character tokens.
BANG = TokenType(TokenType.BANG)
BANG_EQUAL = TokenType(TokenType.BANG_EQUAL)
EQUAL = TokenType(TokenType.EQUAL)
EQUAL_EQUAL = TokenType(TokenType.EQUAL_EQUAL)
GREATER = TokenType(TokenType.GREATER)
GREATER_EQUAL = TokenType(TokenType.GREATER_EQUAL)
LESS = TokenType(TokenType.LESS)
LESS_EQUAL = TokenType(TokenType.LESS_EQUAL)

# Literals.
IDENTIFIER = TokenType(TokenType.IDENTIFIER)
STRING = TokenType(TokenType.STRING)
NUMBER = TokenType(TokenType.NUMBER)

# Keywords.
AND = TokenType(TokenType.AND)
CLASS = TokenType(TokenType.CLASS)
ELSE = TokenType(TokenType.ELSE)
FALSE = TokenType(TokenType.FALSE)
FUN = TokenType(TokenType.FUN)
FOR = TokenType(TokenType.FOR)
IF = TokenType(TokenType.IF)
NIL = TokenType(TokenType.NIL)
OR = TokenType(TokenType.OR)
PRINT = TokenType(TokenType.PRINT)
RETURN = TokenType(TokenType.RETURN)
SUPER = TokenType(TokenType.SUPER)
THIS = TokenType(TokenType.THIS)
TRUE = TokenType(TokenType.TRUE)
VAR = TokenType(TokenType.VAR)
WHILE = TokenType(TokenType.WHILE)

EOF = TokenType(TokenType.EOF)
