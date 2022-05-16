from .. import BotNet, Request


@BotNet.deafult_script(script_version="0.0.1")
def echo(request: Request, stars_count: int, *message) -> str:
    """
    Print message in stdout

    example input command: `echo 5 hi :)`\n
    output: `print("***** hi :) *****")`\n
    return: `"Successfully printed."`
    """

    stars = "*" * int(stars_count)
    print(f"{stars} {' '.join(message)} {stars}")
    return "Successfully printed."
