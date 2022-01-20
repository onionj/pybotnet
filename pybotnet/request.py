
from typing import TYPE_CHECKING, Dict, List


if TYPE_CHECKING:
    from . import BaseEngine


class Request:
    '''requests data: \n
    * engine: "BaseEngine"
    * command: List
    * time_stamp: str
    * sytsem_data: Dict
    * mata_data: Dict'''

    engine: "BaseEngine"
    command: List
    time_stamp: str
    sytsem_data: Dict
    meta_data: Dict
