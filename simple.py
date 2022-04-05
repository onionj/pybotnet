from os import listdir
from pybotnet import BotNet, TestEngine, Request, UserException
from simple_external import script

test_engine = TestEngine([["echo", "10", "hi", ":)"], ["ls"], ["ls", '..'], ['ls', ''], ["echo_meta_data"]])



botnet = BotNet(test_engine, debug=True, use_default_scripts=True)

# create new script
@botnet.add_script()
def ls(request: Request, route="."):
    """get ls"""
    
    if route == '':
        raise UserException('Please send a valid route')

    return listdir(route)


# add external scripts
botnet.import_scripts(script)


if __name__ == "__main__":
    print(botnet)
    botnet.run()
