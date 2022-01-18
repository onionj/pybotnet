from .. import BotNet


@BotNet.add_scripts(script_version="0.0.1")
def echo(stars_count: int, *message):
    """print message \n
    example: `echo_hi 5 hi :)`
    """

    stars = "*" * int(stars_count)
    print(f"{stars} {' '.join(message)} {stars}")
    return "Successfully printed."
