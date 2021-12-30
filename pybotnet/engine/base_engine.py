from abc import ABC
from abc import abstractmethod


from typing import List


class BaseEngine(ABC):
    """This class must be singleton"""

    @abstractmethod
    def __str__(self):
        return "Base Engine"

    @abstractmethod
    def receive(self) -> List[str]:
        """get last admin command"""
        ...

    @abstractmethod
    def send(self, response: str) -> bool:
        """send message to admin"""
        ...
