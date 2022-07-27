from typing import TYPE_CHECKING, Any, Dict, List, Optional
from dataclasses import dataclass

if TYPE_CHECKING:
    from . import BaseEngine


@dataclass
class Context:
    """requests data: \n
    * engine: "BaseEngine"
    * command: List
    * time_stamp: str
    * system_info: callable
    * mata_data: Dict
    * set_global_value: callable
    * get_global_value: callable"""

    engine: "BaseEngine"
    command: List
    time_stamp: str
    system_info: callable
    meta_data: Dict

    _global_values = {}

    @classmethod
    def set_global_value(cls, key, value):
        cls._global_values.update({key: value})

    @classmethod
    def get_global_value(cls, key) ->  Optional[Any]:
        "return value or None"
        return cls._global_values.get(key)

    @classmethod
    def get_all_global_values(cls) -> dict[Any, Any]:
        return cls._global_values