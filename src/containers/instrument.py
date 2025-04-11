# containers/instrument.py

from typing import List
from utils.printable import Printable

class BaseInst(Printable):
    def __init__(self, index: int, name: str): 
        self.index = index
        self.name = name


class Inst2A03(BaseInst):
    def __init__(self, 
        index: int, name: str, 
        vol: int, arp: int, pit: int, hpi: int, dut: int
    ):
        super().__init__(index, name)
        
        self.vol = vol
        self.arp = arp
        self.pit = pit
        self.hpi = hpi
        self.dut = dut
        
        self.macros = {}


class InstVRC7(BaseInst):
    def __init__(self,
        index: int, name: str,
        patch: int, registers: List[int],
    ):
        super().__init__(index, name)
        
        self.patch = patch
        self.registers = registers


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


class InstN163(BaseInst):
    def __init__(self,
        index: int, name: str,
        vol: int, arp: int, pit: int, hpi: int, dut: int,
        w_size: int, w_pos: int, w_count: int
    ):
        super().__init__(index, name)
        
        self.vol = vol
        self.arp = arp
        self.pit = pit
        self.hpi = hpi
        self.dut = dut

        self.w_size = w_size
        self.w_pos = w_pos
        self.w_count = w_count

        self.macros = {}
        
