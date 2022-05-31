import time
import os
from PIL import ImageGrab

from .. import BotNet, Request


@BotNet.default_script(script_version="0.0.1")
def screenshot(request: Request) -> str:
    """get screen shot
    example command: `/screenshot` \n
    return: img or img-download-link
    """

    file_name = f"{str(time.time()).replace('.', '_')}.png"

    with open(file_name, 'wb') as file:
        screenshot = ImageGrab.grab()
        # Save the image to the file object as a PNG
        screenshot.save(file, 'PNG')

    res = request.engine.send_file(file_name)
    os.remove(file_name)

    if res:
        return None
    return "send screen-shot failed!"

