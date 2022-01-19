from functools import wraps
from typing import Dict, Optional
import time
import logging

_logger = logging.getLogger(f"{__name__}")


class BotNet:
    default_scripts = {}

    def __init__(
        self,
        engine=None,
        *,
        version: str = "0.0.1",
        delay: int = 5,
        debug: bool = False,
        **extra,
    ):

        self._debug: bool = debug
        self.version = version
        self.delay = delay
        self.engine = engine
        self.use_default_scripts: bool = True
        self.scripts = {}

        if self.use_default_scripts:
            self.scripts.update(**BotNet.default_scripts)

        if self._debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        _logger.debug(
            f"init botnet, scripts count: {len(self.scripts)}, engine: {self.engine}"
        )

    def __str__(self):
        return f"scripts: {', '.join(self.scripts.keys())}"

    @classmethod
    def deafult_script(cls, *, script_name=None, script_version: Optional[str] = None):
        def decorator(func):

            @wraps(func)
            def wrapper(*args, **kwargs):

                return func(*args, **kwargs)

            wrapper.__name__ = script_name or func.__name__
            wrapper.__doc__ = func.__doc__
            wrapper.__extra__ = {}
            wrapper.__extra__.update({'version': script_version, 'deafult_script': True})

            cls.default_scripts.update({script_name or func.__name__: wrapper})
            return wrapper

        return decorator

    def add_script(self, *, script_name=None, script_version: Optional[str] = None):
        def decorator(func):

            @wraps(func)
            def wrapper(*args, **kwargs):

                return func(*args, **kwargs)

            wrapper.__name__ = script_name or func.__name__
            wrapper.__doc__ = func.__doc__
            wrapper.__extra__ = {}
            wrapper.__extra__.update({'script_version': script_version, 'deafult_script': False})

            self.scripts.update({script_name or func.__name__: wrapper})
            return wrapper

        return decorator

    def run(self):
        while True:
            command = self.engine.receive()
            script = self.scripts.get(command[0])
            if script:
                args = command[1:]

                _logger.debug(
                    f"<BotNet.run: {script.__name__}(Version: {script.__extra__.get('version')}, Doc: '''{script.__doc__}''', Args: {args}))>")

                ret = "NULL"

                try:
                    ret = script(*args)

                except Exception as e:
                    ret = e

                finally:
                    self.engine.send(ret)
                    time.sleep(self.delay)

    def import_scripts(self, external_scripts: "ExternalScripts"):
        self.scripts.update(**external_scripts.scripts)


class ExternalScripts(BotNet):
    def __init__(self):
        self.scripts = {}
