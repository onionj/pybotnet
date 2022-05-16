from os import listdir, getcwd
import logging

from pybotnet import BotNet, TestEngine, Request, UserException
from simple_external import external_botnet

_logger = logging.getLogger(f"{__name__}   ")


test_engine = TestEngine(
    [["echo", "10", "hi", ":)"], ["ls"], ["ls", ".."], ["ls", ""], ["echo_meta_data"]]
)


botnet = BotNet(test_engine, debug=True, use_default_scripts=True)

# create new script
@botnet.add_script(script_version="0.1.0")
def ls(request: Request, route="."):
    """get ls"""

    if route == "":
        raise UserException("Please send a valid route")

    response = f"route: {getcwd()}\n {listdir(route)}"
    return response


# add external scripts
botnet.import_scripts(external_botnet)


if __name__ == "__main__":
    _logger.debug(botnet)
    botnet.run()
