from token_class import Token
import token_type_instances as TT


class AbstractClassInstance(Exception):
    ...


class UndefinedMethod(Exception):
    ...


had_error = False
had_runtime_error = False


def report(line: int, where: str, message: str) -> None:
    print("[line " + str(line) + "] Error" + where + ": " + message)
    global had_error
    had_error = True


def error(line: int, message: str) -> None:
    report(line, "", message)


def token_error(lox_token: Token, message: str) -> None:
    if lox_token.type == TT.EOF:
        report(lox_token.line, " at end", message)
    else:
        report(lox_token.line, " at '" + lox_token.lexeme + "'", message)


def runtime_error(lox_token: Token, message: str) -> RuntimeError:
    print(message + "\n[line " + str(lox_token.line) + "]")
    global had_runtime_error
    had_runtime_error = True
    raise RuntimeError
