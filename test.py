from configs import *
import pybotnet

bot = pybotnet.PyBotNet(TELEGRAM_TOKEN, ADMIN_CHAT_ID, show_log=True)

ans = bot.send_message_by_third_party_proxy('hi admin')
print(ans)
