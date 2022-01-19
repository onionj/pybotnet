from os import listdir
from pybotnet import BotNet, TestEngine
from simple_external import script

test_engine = TestEngine(["echo", "10", "hi", ":)"])
# test_engine = TestEngine(["ls", "/"])


botnet = BotNet(test_engine, debug=False)


@botnet.add_scripts()
def ls(route="."):
    """get ls"""
    return listdir(route)


botnet.import_scripts(script)

print(botnet)

botnet.run()
