# note_events.py

class BaseMidiEvent:
    def __init__(self, track: int, start: int):
        self.track = track
        self.start = start

    def __repr__(self) -> str:
        return "<class {}>".format(self.__class__.__name__)

    def __str__(self) -> str:
        return self.__repr__()


class MidiNoteEvent(BaseMidiEvent):
    def __init__(self, track: int, channel: int, start: int, pitch: int, velocity: int):
        super().__init__(track, start)
        self.channel = channel
        self.pitch = pitch
        self.velocity = velocity
        
        # to be added later?
        self.duration = None
    
    def set_duration(self, time: int) -> int:
        dur = time - self.start
        if dur <= 0:
            raise ValueError("Duration cannot be 0 or negative")
        self.duration = dur
        return dur
    

class MidiBpmEvent(BaseMidiEvent):
    def __init__(self, track: int, start: int, bpm: int):
        super().__init__(track, start)
        self.bpm = bpm    

