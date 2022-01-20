from os import listdir
from pybotnet import BotNet, TestEngine, Request
from simple_external import script

test_engine = TestEngine(["echo", "10", "hi", ":)"])
# test_engine = TestEngine(["ls", "/"])
# test_engine = TestEngine(["echo_meta_data"])


botnet = BotNet(test_engine, debug=True)


@botnet.add_script()
def ls(request: Request, route="."):
    """get ls"""
    return listdir(route)


botnet.import_scripts(script)

print(botnet)

botnet.run()
