from .. import BotNet


@BotNet.deafult_script(script_version="0.0.1")
def echo(stars_count: int, *message):
    """print message \n
    example: `echo 5 hi :)`
    """

    stars = "*" * int(stars_count)
    print(f"{stars} {' '.join(message)} {stars}")
    return "Successfully printed."
