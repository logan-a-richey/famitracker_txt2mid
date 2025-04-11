# containers/inst_fds.py

from containers.base_inst import BaseInst

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
        
        self.macros = {}


