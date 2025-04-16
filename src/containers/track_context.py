# containers/track_context.py

from typing import List

from containers.track import Track
from containers.echo_buffer import EchoBuffer
from containers.column_context import ColumnContext

class TrackContext:
    ''' Contains data for intermediate track variables '''
    def __init__(self, track: Track, target_order: str, target_row: int, orders: List[str], patterns: List[str]):
        self.track = track
        self.target_order = target_order
        self.target_row = target_row
        self.orders = orders
        self.patterns = patterns
        self.echo_buffers = [EchoBuffer() for _ in range(self.track.num_cols)]
        self.col_contexts = [ColumnContext() for _ in range(self.track.num_cols)]
        self.speed: int = self.track.speed


