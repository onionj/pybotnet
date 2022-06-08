
from typing import TYPE_CHECKING, Dict, List


if TYPE_CHECKING:
    from . import BaseEngine


class Request:
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
