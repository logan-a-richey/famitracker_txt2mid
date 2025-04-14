# containers/inst_fds.py

from typing import List, Dict

from containers.base_inst import BaseInst
from containers.macro import Macro

class InstFDS(BaseInst):
    def __init__(self,
        index: int, name: str,
        mod_enable: int, mod_speed: int, mod_depth: int, mod_delay: int
    ):
        super().__init__(index, name)
        
        self.mod_enable = mod_enable
        self.mod_speed = mod_speed
        self.mod_depth = mod_depth
        self.mod_delay = mod_delay
        
        self.macros: Dict[str, Macro] = {}
        
        self.fds_wave: List[int] = []
        self.fds_mod: List[int] = []


