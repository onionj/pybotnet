from .. import BotNet, Request


@BotNet.default_script(script_version="0.0.1")
def echo(request: Request, stars_count: int, *message) -> str:
    """Print message in stdout

    example input command: `/echo 5 hi :)`\n
    output: `print("***** hi :) *****")`\n
    return: `"Successfully printed."`"""

    stars = "*" * int(stars_count)
    msg = f"{stars} {' '.join(message)} {stars}"
    print(msg)
    return f"Successfully printed: `{msg}`"
