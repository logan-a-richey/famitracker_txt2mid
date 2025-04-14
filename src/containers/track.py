# containers/track.py

from typing import List, Dict

from utils.printable import Printable

class Track(Printable):
    '''Store track data'''
    # static variable to assign track indexes upon init
    count = 0 

    def __init__(self):
        Track.count += 1
        self.index = Track.count

        # "public" attributes
        self.name: str = "Default"
        self.speed: int = 6
        self.tempo: int = 150

        self.num_rows: int = 64
        self.num_cols: int = 5
        self.eff_cols: List[int] = [1 for _ in range(self.num_cols)]

        self.orders: Dict[str, List[str]] = {}
        self.patterns: List[str] = []

        # "private" attributes
        # used for loading pattern rows / tokens
        self._target_pattern: str = "00"


