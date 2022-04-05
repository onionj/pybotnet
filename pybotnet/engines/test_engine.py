from typing import List, Union, Literal
from . import BaseEngine


class TestEngine(BaseEngine):
    """Test Engine"""

    instance = None

    def __init__(self, comands: List[List[str]]) -> None:
        self.command = comands

    def __str__(self):
        return "Test Engine"

    def receive(self) -> Union[List[str], Literal[False]]:
        try:
            return self.command.pop()
        except IndexError:
            return False

    def send(self, message):
        print(f"<Test engine sended ({message})>")
