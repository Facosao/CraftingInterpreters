from token_class import Token


class Expr:
    ...


def parenthesize(name: str, exprs: list[Expr]) -> str:
    output = "(" + name

    for expr in exprs:
        output += " "
        output += str(expr)

    output += ")"
    return output


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return parenthesize(self.operator.lexeme, [self.left, self.right])


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr) -> None:
        super().__init__()
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return parenthesize(self.operator.lexeme, [self.right])


class Grouping(Expr):
    def __init__(self, expression: Expr) -> None:
        super().__init__()
        self.expression = expression

    def __str__(self):
        return parenthesize("group", [self.expression])


class Literal(Expr):
    def __init__(self, value: object) -> None:
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        if self.value == None:
            return "nil"
        else:
            return str(self.value)
