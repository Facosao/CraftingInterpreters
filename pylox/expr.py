from token_class import Token
import token_type_instances as TT
import error


def LoxRuntimeError(lox_token: Token, message: str) -> RuntimeError:
    error.runtime_error(lox_token, message)
    raise RuntimeError


class AbstractClassInstance(Exception):
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


def check_operand(operator: Token, operand: object) -> float:
    if isinstance(operand, float):
        return operand

    raise LoxRuntimeError(operator, "Operand must be a number.")


def check_operands(operator: Token, left: object, right: object) -> tuple[float, float]:
    if isinstance(left, float) and isinstance(right, float):
        return left, right

    raise LoxRuntimeError(operator, "Operands must be a number.")


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
                left, right = check_operands(self.operator, left, right)
                return left - right
            case TT.SLASH:
                left, right = check_operands(self.operator, left, right)
                return left / right
            case TT.STAR:
                left, right = check_operands(self.operator, left, right)
                return left * right
            case TT.GREATER:
                left, right = check_operands(self.operator, left, right)
                return left > right
            case TT.GREATER_EQUAL:
                left, right = check_operands(self.operator, left, right)
                return left >= right
            case TT.LESS:
                left, right = check_operands(self.operator, left, right)
                return left < right
            case TT.LESS_EQUAL:
                left, right = check_operands(self.operator, left, right)
                return left <= right
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
                    raise LoxRuntimeError(
                        self.operator, "Operands must be two numbers or two strings."
                    )

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
                right = check_operand(self.operator, right)
                return 0 - right

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
