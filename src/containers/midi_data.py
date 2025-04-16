# containers/midi_data.py

from typing import List
from containers.note_event_structs import NoteEvent, TempoEvent, TimeSigEvent

class MidiData:
    ''' Holds Midi data '''
    def __init__(self):
        self.note_on_events: List[NoteEvent] = []
        self.tempo_events: List[TempoEvent] = []
        self.time_sig_events: List[TimeSigEvent] = []
