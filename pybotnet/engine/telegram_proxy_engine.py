from .base_engine import BaseEngine

from typing import List


class TelegramProxyEngine(BaseEngine):
    _instance = None

    def __new__(cls):
        pass

    def __init__(self, TOKEN: str, CHAT_ID: str, *args, **kwargs) -> None:
        self.TOKEN = TOKEN
        self.CHAT_ID = CHAT_ID

    def __str__(self):
        return f"<TOKEN:({self.TOKEN}), CHAT_ID:({self.CHAT_ID})>"

    def receive(self) -> List[str]:
        ...

    def send(self, response: str) -> bool:
        ...
