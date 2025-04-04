# instrument.py

from typing import List
from printable import Printable

class BaseInst(Printable):
    def __init__(
        self,
        index: int, 
        name: str, 
        chip: str
    ):
        self.index = index
        self.name = name
        self.chip = chip


class Inst2a03(BaseInst):
    def __init__(
        self, 
        index: int,
        name: str,
        chip: str,
        
        seq_vol: int,
        seq_arp: int,
        seq_pit: int,
        seq_hpi: int,
        seq_dut: int
    ):
        super().__init__(index, name, chip)
        #super(BaseInst).__init__(index, name, chip)
        self.seq_vol = seq_vol
        self.seq_arp = seq_arp
        self.seq_pit = seq_pit
        self.seq_hpi = seq_hpi
        self.seq_dut = seq_dut
        
        # to be loaded later
        self.macros = {
            "vol": None,
            "arp": None,
            "pit": None,
            "hpi": None,
            "dut": None
        }


class InstVrc7(BaseInst):
    def __init__(
        self,
        index: int,
        name: str,
        chip: str,
        
        patch: int,
        registers: List[str]
    ):
        super().__init__(index, name, chip)
        self.patch = patch
        self.registers = registers


class InstFds(BaseInst):
    def __init__(
        self,
        index: int, 
        name: str, 
        chip: str, 
        
        mod_enable: int, 
        mod_speed: int, 
        mod_depth: int, 
        mod_delay: int
    ):
        super().__init__(index, name, chip)
        self.mod_enable = mod_enable
        self.mod_speed = mod_speed
        self.mod_depth = mod_depth
        self.mod_delay = mod_delay


class InstN163(Inst2a03):
    def __init__(
        self,
        index: int,
        name: str,
        chip: str,
        
        seq_vol: int,
        seq_arp: int,
        seq_pit: int,
        seq_hpi: int,
        seq_dut: int,
        
        w_size: int,
        w_pos: int,
        w_count: int
    ):
        super().__init__(index, name, chip, seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut)
        self.w_size = w_size
        self.w_pos = w_pos
        self.w_count = w_count


