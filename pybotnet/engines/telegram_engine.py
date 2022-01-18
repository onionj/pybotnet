from .base_engine import BaseEngine

from typing import List


class TelegramEngine(BaseEngine):

    _instance = None

    def __new__(cls, *args, **kwargs):
        """singleton class"""
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.is_initialized = False
        return cls._instance

    def __init__(
        self, TOKEN: str = None, CHAT_ID: str = None, proxy: bool = False
    ) -> None:
        if not self.is_initialized:
            self.TOKEN = TOKEN
            self.CHAT_ID = CHAT_ID
            self._proxy = proxy
            if None in [self.TOKEN, self.CHAT_ID]:
                raise Exception("Initialize TOKEN and CHAT_ID")

            self.is_initialized = True

    def __str__(self):
        return f"<TOKEN:({self.TOKEN}), CHAT_ID:({self.CHAT_ID})>"

    def receive(self) -> List[str]:
        ...

    def send(self, response: str) -> bool:
        ...
