
from typing import TYPE_CHECKING, Dict, List


if TYPE_CHECKING:
    from . import BaseEngine


class Context:
    '''requests data: \n
    * engine: "BaseEngine"
    * command: List
    * time_stamp: str
    * system_info: callable
    * mata_data: Dict'''
    
    engine: "BaseEngine"
    command: List
    time_stamp: str
    system_info: callable
    meta_data: Dict

    
    _global_values = {}

    def set_global_value(self, key, value):
        self._global_values.update({key, value})

    def get_global_value(self, key):
        return self._global_values.get(key)
