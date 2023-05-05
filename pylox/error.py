def report(line: int, where: str, message: str, error_var) -> None:
    print("[line " + str(line) + "] Error" + where + ": " + message)
    error_var = True


def error(line: int, message: str, error_var: bool) -> None:
    report(line, "", message, error_var)
