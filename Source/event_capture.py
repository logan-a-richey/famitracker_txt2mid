
class NoteEvent:
    def __init__(self,
        track: int,
        start: int,
        duration: int,
        pitch: int,
        vol: int
    ):
        self.track      = track
        self.start      = start
        self.duration   = duration
        self.pitch      = pitch
        self.vol        = vol

class EventCapture:
    def __init__(self):
        self.events = {}

