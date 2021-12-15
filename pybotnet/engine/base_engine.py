from abc import ABC
from abc import abstractmethod


from typing import List


class BaseEngine(ABC):
    """This class must be singleton"""

    @abstractmethod
    def get_command(self) -> List[str]:
        """get last admin command"""
        ...

    @abstractmethod
    def post_response(self, response: str) -> bool:
        """send message to admin"""
        ...
