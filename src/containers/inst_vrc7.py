# containers/inst_vrc7.py

from typing import List
from containers.base_inst import BaseInst

class InstVRC7(BaseInst):
    def __init__(self,
        index: int, name: str,
        patch: int, registers: List[int],
    ):
        super().__init__(index, name)
        
        self.patch = patch
        self.registers = registers


