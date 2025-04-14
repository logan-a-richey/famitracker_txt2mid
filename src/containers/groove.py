# groove.py

from typing import List

from utils.printable import Printable

class Groove(Printable):
    def __init__(self, index: int, sizeof: int, sequence: List[int]):
        self.index = index
        self.sizeof = sizeof
        self.sequence = sequence


