# conainters/inst_n163.py

from containers.base_inst import BaseInst

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
        self.n163_waves = {} 
