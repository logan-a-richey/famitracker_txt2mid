# note event structs

class NoteEvent:
    def __init__(self, midi_track: int, midi_channel: int, start_tick: int, duration_tick: int, pitch: int, volume: int):
        self.midi_track = midi_track
        self.midi_channel = midi_channel
        self.start_tick = start_tick
        self.duration_tick = duration_tick
        self.pitch = pitch
        self.volume = volume
        
class TempoEvent:
    def __init__(self):
        pass

class TimeSigEvent:
    def __init__(self):
        pass

