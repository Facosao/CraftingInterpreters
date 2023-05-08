from token_class import Token
import token_type_instances as TT


class OperandCastError(RuntimeError):
    ...


class AbstractClassInstance(RuntimeError):
    ...


class Expr:
    def __init__(self) -> None:
        raise AbstractClassInstance

    def interpret(self) -> object:
        pass


def parenthesize(name: str, exprs: list[Expr]) -> str:
    output = "(" + name

    for expr in exprs:
        output += " "
        output += str(expr)

    output += ")"
    return output


def stringify(lox_object: object) -> str:
    if lox_object is None:
        return "nil"

    if isinstance(lox_object, bool):
        if lox_object is True:
            return "true"
        else:
            return "false"

    if isinstance(lox_object, float):
        text = str(lox_object)
        if text.endswith(".0"):
            text = text[0 : len(text) - 2]

        return text

    return str(lox_object)


def is_truthy(test_obj: object) -> bool:
    if object == None:
        return False
    if isinstance(test_obj, bool) is True:
        return bool(test_obj)

    return True


def is_equal(obj_a: object, obj_b: object) -> bool:
    if (obj_a is None) and (obj_b is None):
        return True
    if obj_a is None:
        return False

    return obj_a == obj_b


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return parenthesize(self.operator.lexeme, [self.left, self.right])

    def interpret(self) -> object:
        left: object = self.left.interpret()
        right: object = self.right.interpret()

        match self.operator.type:
            case TT.MINUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) - float(right)
                else:
                    raise OperandCastError
            case TT.SLASH:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) / float(right)
                else:
                    raise OperandCastError
            case TT.STAR:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) * float(right)
                else:
                    raise OperandCastError
            case TT.GREATER:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) > float(right)
                else:
                    raise OperandCastError
            case TT.GREATER_EQUAL:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) >= float(right)
                else:
                    raise OperandCastError
            case TT.LESS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) < float(right)
                else:
                    raise OperandCastError
            case TT.LESS_EQUAL:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) <= float(right)
                else:
                    raise OperandCastError
            case TT.BANG_EQUAL:
                return not is_equal(left, right)
            case TT.EQUAL_EQUAL:
                return is_equal(left, right)
            case TT.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                elif isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                else:
                    raise OperandCastError

        return None


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr) -> None:
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return parenthesize(self.operator.lexeme, [self.right])

    def interpret(self) -> object:
        right: object = self.right.interpret()

        match self.operator.type:
            case TT.BANG:
                return not is_truthy(right)
            case TT.MINUS:
                if isinstance(right, float):
                    return 0 - float(right)
                else:
                    raise OperandCastError

        return None


class Grouping(Expr):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def __str__(self):
        return parenthesize("group", [self.expression])

    def interpret(self) -> object:
        return self.expression.interpret()


class Literal(Expr):
    def __init__(self, value: object) -> None:
        self.value = value

    def __str__(self) -> str:
        if self.value == None:
            return "nil"
        else:
            return str(self.value)

    def interpret(self) -> object:
        return self.value
