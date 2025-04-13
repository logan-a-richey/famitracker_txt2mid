# containers/dpcm.py

from typing import List

from utils.printable import Printable

class Dpcm(Printable):
    def __init__(self, index: int, size: int, name: str):
        self.index = index
        self.size = size
        self.name = name

        self.data: List[int] = []
