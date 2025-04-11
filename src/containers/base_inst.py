# containers/base_inst.py

from utils.printable import Printable

class BaseInst(Printable):
    def __init__(self, index: int, name: str): 
        self.index = index
        self.name = name


