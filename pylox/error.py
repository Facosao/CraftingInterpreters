from token_class import Token
import token_type_instances as TT


def report(line: int, where: str, message: str, error_var) -> None:
    print("[line " + str(line) + "] Error" + where + ": " + message)
    error_var = True


def error(line: int, message: str, error_var: bool) -> None:
    report(line, "", message, error_var)


def token_error(lox_token: Token, message: str, error_var) -> None:
    if lox_token.type == TT.EOF:
        report(lox_token.line, " at end", message, error_var)
    else:
        report(lox_token.line, " at '" + lox_token.lexeme + "'", message, error_var)
