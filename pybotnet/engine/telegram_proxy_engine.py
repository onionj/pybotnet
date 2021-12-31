from .base_engine import BaseEngine

from typing import List


class TelegramProxyEngine(BaseEngine):

    _instance = None

    def __new__(cls, TOKEN: str = None, CHAT_ID: str = None):
        """singleton class"""
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.is_initialized = False
        return cls._instance

    def __init__(self, TOKEN: str = None, CHAT_ID: str = None) -> None:
        if not self.is_initialized:

            self.TOKEN = TOKEN
            self.CHAT_ID = CHAT_ID

            if None in (required_args := [self.TOKEN, self.CHAT_ID]):
                raise TypeError(
                    f" __init__() missing {required_args.count(None)} required positional arguments: (required args: 'TOKEN', 'CHAT_ID')"
                )

            self.is_initialized = True

    def __str__(self):
        return f"<TOKEN:({self.TOKEN}), CHAT_ID:({self.CHAT_ID})>"

    def receive(self) -> List[str]:
        ...

    def send(self, response: str) -> bool:
        ...
