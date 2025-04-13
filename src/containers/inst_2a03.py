# containers/inst_2a03.py

from containers.base_inst import BaseInst

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
        self.key_dpcm = {}

