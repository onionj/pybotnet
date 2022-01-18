from pybotnet import BotNet, TestEngine
from os import listdir

test_engine = TestEngine(["echo", "10", "hi", ":)"])


botnet = BotNet(test_engine, debug=False)


@botnet.add_scripts()
def ls(route="."):
    """get ls"""
    return listdir(route)


print(botnet)

botnet.run()
