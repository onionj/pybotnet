from .. import BotNet, Request


@BotNet.default_script(script_version="0.0.1")
def echo(request: Request) -> str:
    """Print message in stdout

    example input command: `/echo hi :)`\n
    output: `print("hi")`\n
    return: `"Successfully printed."`"""

    msg = ' '.join(request.command)
    print(msg)
    return f"Successfully printed: `{msg}`"
