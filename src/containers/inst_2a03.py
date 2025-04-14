# containers/inst_2a03.py

from typing import Dict

from containers.base_inst import BaseInst
from containers.macro import Macro
from containers.key_dpcm import KeyDpcm

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
        
        self.macros: Dict[str, Macro] = {}
        self.key_dpcm: Dict[int, KeyDpcm] = {}

