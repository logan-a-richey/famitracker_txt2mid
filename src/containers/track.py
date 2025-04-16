# containers/track.py

from typing import List, Dict
from containers.echo_buffer import EchoBuffer

class Track:
    '''Store track data'''
    # static variable to assign track indexes upon init
    count = 0 

    def __init__(self, num_rows: int = 64, speed: int = 6, tempo: int = 150, name: str = "Default"):
        Track.count += 1
        self.index = Track.count

        self.name: str = name
        self.speed: int = speed
        self.tempo: int = tempo

        self.num_rows: int = num_rows
        self.num_cols: int = 5
        self.eff_cols: List[int] = [1 for _ in range(self.num_cols)]

        self.orders: Dict[str, List[str]] = {}
        self.patterns: List[str] = []
        self.tokens: Dict[str, str] = {}
        self._target_pattern: str = "00"

    def __str__(self):
        return "<class {}>, index: {}, name: {}".format(
            self.__class__.__name__, 
            self.index, 
            self.name
        )
