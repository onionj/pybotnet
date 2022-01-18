from typing import List
from . import BaseEngine


class TestEngine(BaseEngine):
    """Test Engine"""

    instance = None

    def __init__(self, comands: List) -> None:
        self.command = comands

    def __str__(self):
        return "Test Engine"

    def receive(self):
        return self.command

    def send(self, message):
        print(f"<Test engine sended ({message})>")
