
### Add custom scripts
This functionality is for when you want to add your own script.

The simplest PyBotNet custom script looks something like this:


```py title="main.py"

from pybotnet import BotNet, Context, TelegramEngine


telegram_engine = TelegramEngine(token=TELEGRAM_TOKEN, admin_chat_id=ADMIN_CHAT_ID) #(1)

botnet = BotNet(telegram_engine) # (2)

# new:
@botnet.add_script(script_version="0.1.0") # (3)
def ping(context: Context):
    """`/ping`"""
    response = f"pong {' '.join(context.command)}" # (4)
    return response # (5)

botnet.run() # (6)

```

1. Create engine: Engines transfer messages between user and botnet
2. Create BotNet instance
3. Create new custom script 
4. Get user command from context and join it to `"pong"`, for example, if user sends `/ping foo bar` the `response` will be `pong foo bar`
5. Return response to user
6. Run main loop

As you can see,  We used a decorator to add our script to the botnet instance, now if we execute the code we have access to the ping script in the control panel.

Scripts can also contain Context parameters, which include the engine itself, system data, commands sent by the user, and so on.

!!! note
    * Context is an optional parameter and if you do not include Context in your function, nothing will happen, but you won't have access to the data sent by the user.
    * If you return `None`, Nothing will be sent back to the user.

#### add_script decorator

The program reads the function name and saves it as script name, but you can change the name by setting the script_name variable in the decorator.


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

1. Change script name from default (`ping`) to `1ping`

#### Context
There are the variables and methods you can use in Context.
* command: List
    - For example in the above code if the user sends `/1ping foo bar`, `context.command` will return this list: `["foo", "bar"]`

* time_stamp: str
    - context creation time

* system_info: callable
    - This method returns the target system info, for example:
        `context.system_info()` returns this data:
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
    - Another method:
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
    - This variable returns the active engine, engines have `send()`, `receive()` and `send_file()` methods;
        You can use them to communicate with the user.

    - `send` method takes two parameter, a string (required) and dict (optional) for adding it to the submessagse
        You can send `context.system_info(minimal=True)` to the second parameter

    - `send_file` like `send` method takes two parametr, first parametr gets the route of the file (required), and the second takes a dict (optional) for add it to sub of message..

    - `recive` return not procesed admin command as a list of string, and if not found new admin command, return `False`

* meta_data: dict
    - this variable contains current `script_name`, `script_version` and `script_doc` 

* set_global_value: callable
    - With this method you can save data in memory, The data is cleared when the botnet is closed ‍‍(This is just a dict!)

* get_global_value: callable
    - Takes a key and returns the data


#### UserException

If input data from user (PyBotNet gets it from `context.command` or in script call `context.engine.recive()`) was not valid, PyBotNet will raise an `UserException` say: `raise UserException("the reason")` 

PyBotNet `simple_serializer` to validate user input data, this function checks len, type of the data and if is ok return a list of converted command by new types..


```py title="main.py"

from pybotnet import BotNet, Context, TelegramEngine, simple_serializer # (1)

telegram_engine = TelegramEngine(token=TELEGRAM_TOKEN, admin_chat_id=ADMIN_CHAT_ID)
botnet = BotNet(telegram_engine)

@botnet.add_script()
def echo(context: Context):
    """`/echo <number> <world>`"""

    command, err = simple_serializer(context.command, [int, str]) # (2)
    if err: 
        raise UserException(err) # (3)

    # (4)
    number = command[0]
    world = command[1]

    for _ in range(number):
        print(world)
    # (5)

botnet.run()
```

1. Import simple_serializer from pybotnet
2. PyBotNet sends user command with excepted types to simple_serializer
3. Send error details user
4. This is the data returned from simple_serializer, and it has new data types.
5. This script dosen't return anything, (by default python returns `None`) so it won't send back any responses to the user
