
you can change some config from `BotNet` class

example:


```py title="main.py"

from pybotnet import BotNet, TelegramEngine


telegram_engine = TelegramEngine(token=TELEGRAM_TOKEN, admin_chat_id=ADMIN_CHAT_ID)

botnet = BotNet(
    telegram_engine, # (1)
    bot_name="onion!", # (2)
    version="1.0.0", # (3)
    delay=1.5, # (4)
    use_default_scripts=True, # (5)
    start_end_notify=True, # (6)
    debug=False # (7)
    )

botnet.run()
```

1. Positional parameter engine
2. Custom name for this instance
3. just a version!
4. sleep in main_loop
5. use build in scripts, default is `True`
6. Send a message to the admin when the program is running or stopped, default is `True`
7. show logs by log level `debug`!, default is `False`