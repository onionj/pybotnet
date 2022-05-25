from .. import BotNet, Request


@BotNet.default_script(script_version="0.0.1")
def who(request: Request) -> str:
    """return system info \n `/who`"""

    info = ""

    for k, v in request.sytsem_data.items():
        info += f"\n{k}: {v}"
    return info
