from configs import *
import util
import pybotnet
import logging

show_log = True

# logging:
if show_log:
    # show all log's
    log_level = logging.INFO
else:
    # off all log's
    log_level = 100
my_logger = logging
my_logger.basicConfig(level=log_level)
logger = my_logger.getLogger('PyBotNet')


bot = pybotnet.PyBotNet(TELEGRAM_TOKEN, ADMIN_CHAT_ID, show_log=show_log)

print(bot.get_last_command_by_third_party_proxy())
