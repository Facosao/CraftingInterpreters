import sys
import expr
import stmt
import error
from scanner import Scanner
from parser_class import Parser
from token_class import Token


def run_file(script: str) -> None:
    file_handler = open(script, "r")
    source_code = file_handler.read(-1)
    file_handler.close()
    try:
        run(source_code)
    except RuntimeError:
        pass

    if error.had_error is True:
        sys.exit(65)

    if error.had_runtime_error is True:
        sys.exit(70)


def run_prompt() -> None:
    while True:
        try:
            user_input = input("> ")
            run(user_input)
            error.had_error = False
        except RuntimeError:
            continue
        except EOFError:
            break


def run(code: str) -> None:
    scanner = Scanner(code)
    tokens: list[Token] = scanner.scan_tokens()
    parser = Parser(tokens)
    statements = parser.parse()

    for statement in statements:
        statement.interpret()

    """
    print(expression)
    if isinstance(expression, expr.Expr):
        value = expression.interpret()
        print(expr.stringify(value))
    """


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: python lox.py [script]")
        sys.exit(64)
    else:
        if len(sys.argv) == 2:
            run_file(sys.argv[1])
        else:
            run_prompt()
