# track.py

from printable import Printable

class Track(Printable):
    def __init__(self, num_rows: int, speed: int, tempo: int, name: str):
        self.num_rows = num_rows
        self.speed = speed
        self.tempo = tempo
        self.name = name

        # data to be added after init
        self.num_cols = 5
        self.eff_cols = [1 for _ in range(5)]

        self.orders = {}
        self.patterns = {}

        self.resequenced_lines = []
        
