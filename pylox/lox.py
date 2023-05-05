import sys
from scanner import Scanner
from token_class import Token

had_error = False


def run_file(script: str) -> None:
    file_handler = open(script, "r")
    source_code = file_handler.read(-1)
    file_handler.close()
    run(source_code)

    if had_error is True:
        sys.exit(65)


def run_prompt() -> None:
    while True:
        try:
            user_input = input("> ")
            run(user_input)
            had_error = False
        except EOFError:
            break


def run(code: str) -> None:
    scanner = Scanner(code, had_error)
    tokens: list[Token] = scanner.scan_tokens()
    for token in tokens:
        print(token)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: pylox [script]")
        sys.exit(64)
    else:
        if len(sys.argv) == 2:
            run_file(sys.argv[1])
        else:
            run_prompt()
