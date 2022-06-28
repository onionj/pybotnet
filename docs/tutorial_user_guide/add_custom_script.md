
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
    response = f"pong {' '.join(context.command)}" # (6)
    return response # (7)

botnet.run() # (8)

```

1. create engine: Engines transfer messages between admin and botnet
2. create BotNet instance
3.  create new custom script 
4. we import Context to recive requests and system data
5. get context
6. get admin command from context and join to `"pong"`, if admin send `/ping foo bar` so `response` is `pong foo bar`
7. return response to admin
7. run main loop


In the code above, we added a script that returns `pong <message>` for us when we execute the `\ping <message>` comment.

As you see. We used a decorator to add our script to the botnet instance, now if we execute the code we have access to the ping script in the control panel.

Scripts can also contain Context parameters, which include the engine itself, system data, commands sent by the user, and so on.

!!! note
    * Context is an optional parameter and if you do not include Context in your function, nothing will happen, but in this case you do not have access to the data inside it.
    * If you return `None`, it will not send this to the admin (no response)

#### add_script decorator

the program reads the function name and saves it as script name, but you can change the name by set the script_name variable to the decorator.


```py title="main.py"

from pybotnet import BotNet, Context, TelegramEngine


telegram_engine = TelegramEngine(token=TELEGRAM_TOKEN, admin_chat_id=ADMIN_CHAT_ID)

botnet = BotNet(telegram_engine)

# new:
@botnet.add_script(script_version="0.1.0", script_name="1ping") # (1)
def ping(context: Context):
    """`/1ping`"""
    return f"pong {' '.join(context.command)}"


botnet.run()
```

1. change script name from default (`ping`) to `1ping`

#### Context

Context has a series of useful variables and methods:


* command: List
    - For example in above code if the user send `/1ping foo bar`, `context.command` return this list: `["foo", "bar"]`

* time_stamp: str
    context creation time

* system_info: callable
    - this method return a Dict as target system info, if you call it like this:
        `context.system_info()` return this data:
        ```
        scripts_name
        mac_addres
        os
        global_ip
        bot_name
        local_ip
        host_name
        system_user
        up_time
        current_route
        pid
        cpu_count
        pybotnet_version
        
        ```
    - and if you call this like this
        `context.system_info(minimal=True)` return just minimal data:
        ```
        scripts_name
        mac_addres
        os
        global_ip
        bot_name
        ```
    - system_info method cache data for 30s 


* engine:
    - This variable returns the active engine, engins have `send()`, `receive()` and `send_file()` methods;
        You can use them to communicate with the admin.

    - `send` method get two parameter, first a string (required), second is a Dict (optional) for add it to sub of message
        you can send `context.system_info(minimal=True)` to second parameter

    - `send_file` like `send` method have two parametr, first parametr get route of file (required),  second is a Dict (optional) for add it to sub of message..

    - `recive` return not procesed admin command as a list of string, and if not found new admin command, return `False`

* mata_data: Dict
    - this variable contain courent `script_name`, `script_version` and `script_doc` 

* set_global_value: callable
    - With this method you can save data in memory, The data is cleared when the botnet is closed ‍‍(This is just a Dict!)

* get_global_value: callable
    - Takes a key and returns the data


#### UserException

for example if input data from admin (we get it from `context.command` or in script call `context.engine.recive()`) not valid... we can `raise` as `UserException` like: `raise UserException("the reason")` 

we can use `simple_serializer` to validate user input data, this function check len, type of data and if is ok return a list of converted command by new types..


```py title="main.py"

from pybotnet import BotNet, Context, TelegramEngine, simple_serializer # (1)

telegram_engine = TelegramEngine(token=TELEGRAM_TOKEN, admin_chat_id=ADMIN_CHAT_ID)
botnet = BotNet(telegram_engine)

@botnet.add_script()
def echo(context: Context):
    """`/echo <number> <world>`"""

    command, err = simple_serializer(context.command, [int, str]) # (2)
    if err: # (3)
        raise UserException(err) # (4)

    # (5)
    number = command[0]
    world = command[1]

    for _ in range(number):
        print(world)
    # (6)

botnet.run()
```

1. import simple_serializer from pybotnet
2. we send user command and excepted types to simple_serializer
3. if err not `None`
4. send detail from bad value and script data to admin
5. this data returned from simple_serializer, and have new data types..
6. as you see we don't return anything, (by default python return`None`) so this script don't have response for admin 