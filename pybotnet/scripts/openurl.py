import webbrowser

from .. import BotNet, Context, UserException
from ..utils import simple_serializer


@BotNet.default_script(script_version="0.0.1")
def openurl(context: Context) -> str:
    """
    open a specified url n times

    syntax:
        `/openurl <url> <how-many-times>`
        or
        `[mac-address] /openurl <url> <how-many-times>`
        or
        `[BOT-NAME] /openurl <url> <how-many-times>`

    example command:
        `/openurl https://google.com 3` \n

    Note that on some platforms, trying to open a filename using this script,
     may work and start the operating system1s associated program
    """

    command, err = simple_serializer(context.command, [str, int])
    if err:
        raise UserException(err)

    url = command[0]
    times = command[1]

    for _ in range(times):
        webbrowser.open(url,new=0, autoraise=True)
    
    return f"Opened {url}, for {times} times"
