from typing import List, Union, Literal
from . import BaseEngine


class TestEngine(BaseEngine):
    """Test Engine"""

    def __init__(self, comands: List[List[str]]) -> None:
        self.command = comands

    def __str__(self):
        return "Test Engine"

    def receive(self) -> Union[List[str], Literal[False]]:
        try:
            return self.command.pop()
        except IndexError:
            return False

    def send(self, message: str, additionalـinfo:str="", reply_to_last_message: bool = False) -> bool:
        print(f"<TestEngine.send: ({message} {additionalـinfo})>")
        return True

    def send_file(self, file_route: str) -> bool:
        print(f"<TestEngine.send_file: ({file_route})>")
        return True
