
### Add custom scripts

in some case you need to add your own custom scripts

The simplest PyBotNet custom script could look like this:


```py title="main.py"

from pybotnet import BotNet, Context, TelegramEngine # (4)


telegram_engine = TelegramEngine(token=TELEGRAM_TOKEN, admin_chat_id=ADMIN_CHAT_ID) #(1)

botnet = BotNet(telegram_engine) # (2)

# new:
@botnet.add_script(script_version="0.1.0") # (3)
def ping(context: Context): # (5)
    """`/ping`"""
    return f"pong {' '.join(context.command)}" # (6)


botnet.run()

```

1. create engine: Engines transfer messages between admin and botnet
2. create BotNet instance
3.  create new custom script 
4. we import Context to recive requests and system data
5. get context
6. get admin command from context and return it to admin!

In the code above, we added a script that returns `pong <message>` for us when we execute the `\ping <message>` comment.

As you see. We used a decorator to add our script to the botnet instance, now if we execute the code we have access to the ping script in the control panel.

Scripts can also contain Context parameters, which include the engine itself, system data, commands sent by the user, and so on.


