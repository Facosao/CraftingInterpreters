import sys

__had_error = False


def run_file(script: str) -> None:
    file_handler = open(script, "r")
    source_code = file_handler.read(-1)
    file_handler.close()
    run(source_code)

    if __had_error is True:
        sys.exit(65)


def run_prompt() -> None:
    while True:
        try:
            user_input = input("> ")
            run(user_input)
            __had_error = False
        except EOFError:
            break


def run(code: str) -> None:
    print(code)


def report(line: int, where: str, message: str) -> None:
    print("[line " + str(line) + "] Error" + where + ": " + message)
    __had_error = True


def error(line: int, message: str) -> None:
    report(line, "", message)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Usage: pylox [script]")
        sys.exit(64)
    else:
        if len(sys.argv) == 1:
            run_file(sys.argv[0])
        else:
            run_prompt()
