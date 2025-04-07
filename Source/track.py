# track.py

from typing import List, Dict

from printable import Printable

class Track(Printable):
    # static count variable
    index = 0

    def __init__(self, num_rows: int, speed: int, tempo: int, name: str):
        # init variables
        self.num_rows = num_rows
        self.speed = speed
        self.tempo = tempo
        self.name = name
        
        # update static variable
        Track.index += 1
        self.index = Track.index

        # data to be added after init
        self.num_cols = 5
        self.eff_cols = [1 for _ in range(5)]

        self.orders: Dict[str, List[str]] = {}
        self.patterns: Dict[str, Dict[int, List[str]]] = {}
        
        # resequenced rows
        self.data: List[List[str]] = []

