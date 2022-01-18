from functools import wraps
from typing import Dict, Optional
import time
import logging

_logger = logging.getLogger(f"{__name__}")


class BotNet:
    _scripts = {}

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

        if self._debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        _logger.debug(
            f"init botnet, scripts count: {len(BotNet._scripts)}, engine: {self.engine}"
        )

    def __str__(self):
        return "scripts: " + ", ".join(BotNet._scripts.keys())

    @classmethod
    def add_scripts(cls, *, script_name=None, script_version: Optional[str] = None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):

                return func(*args, **kwargs)

            wrapper.__name__ = script_name or func.__name__
            wrapper.__doc__ = func.__doc__
            wrapper.__version__ = script_version
            cls._scripts.update({script_name or func.__name__: wrapper})
            return wrapper

        return decorator

    def run(self):
        while True:
            command = self.engine.receive()
            script = BotNet._scripts.get(command[0])
            if script:

                args = command[1:]

                _logger.debug(
                    f"""<BotNet.run: {script.__name__}(Version: {script.__version__}, Doc: '''{script.__doc__}''', Args: {args}))>"""
                )

                ret = "NULL"

                try:
                    ret = script(*args)

                except Exception as e:
                    ret = e

                finally:
                    self.engine.send(ret)
                    time.sleep(self.delay)
