# track.py

from typing import Dict, List, Tuple

class Track:
    count = 0
    def __init__(self, num_rows: int, speed: int, tempo: int, name: str):
        Track.count += 1
        self.index = Track.count

        self.num_rows   = num_rows
        self.speed      = speed
        self.tempo      = tempo
        self.name       = name

        self.num_cols = 5
        self.eff_cols = [1 for _ in range(self.num_cols)]
       
        self.orders: Dict[str, List[str]] = {}
        self.tokens: Dict[Tuple[int, int, int], str] = {}

    def __str__(self):
        return "<class {}>".format(self.__class__.__name__)
