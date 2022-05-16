from .base_engine import BaseEngine

from typing import List


class TelegramEngine(BaseEngine):
    def __init__(
        self, token: str = None, CHAT_ID: str = None, use_proxy: bool = False
    ) -> None:
        self.token = token
        self.CHAT_ID = CHAT_ID
        self._proxy = use_proxy

    def __str__(self):
        return f"<TOKEN:({self.token}), CHAT_ID:({self.CHAT_ID})>"

    def receive(self) -> List[str]:
        ...

    def send(self, message: str) -> bool:
        ...

    def send_file(self, file_route: str) -> bool:
        ...
