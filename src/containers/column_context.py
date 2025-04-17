# containers/column_context.py

from typing import Dict, Union, Any

class ColumnContext:
    ''' Contains data for '''
    def __init__(self):
        self.tick: int = 0
        self.pitch: Union[int, None] = None
        self.inst: Union[int, None] = 0
        self.vol: Union[int, None] = 15
        self.effects: Dict[str, Any] = {}

        self.pitch_ticks: int = 0
        self.pitch_release_ticks: int = -1

    def set_note_on(self, pitch: int):
        self.pitch = pitch
        self.pitch_ticks = 0
        self.pitch_release_ticks = -1

    def set_note_off(self):
        self.pitch = None
        self.pitch_ticks = 0
        self.pitch_release_ticks = -1


