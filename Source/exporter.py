# exporter.py

import re
import os

from singleton import singleton
from midi_writer import MidiWriter

os.makedirs("Exports", exist_ok=True)

# TODO
# durations
# velocities
# contribute to drum channel
# BPM, speed, grooves
# Qxx and Rxx note bend effects
# Sxx and Gxx note cut and note delay effects (will fix tuplets)
# Macros in between rows (famitracker ticks)
# Logger and settings for all of this stuff
# Python Flask Web application GUI

class ColData:
    def __init__(self):
        self.last_midi_pitch = None
        self.last_instrument = 0
        self.last_volume = 120
        self.last_arpeggio = []

@singleton
class Exporter:
    def __init__(self, project):
        self.project = project
        self.col_data = []

        self.midi = None
        self.current_tick = 0
        self.tick_subdivision = 480 / 8
        self.note_mapping = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
        
    def note_str_to_int(self, token, transpose=0):
        note_int = self.note_mapping.get(token[0], 0)
        accidental = token[1]
        octave = int(token[2]) + 1

        midi_int = (octave * 12) + note_int + transpose
        midi_int = (midi_int + 1) if (accidental == "#") \
            else (midi_int - 1) if (accidental == "b") \
            else midi_int
        
        return midi_int

    def _process_line(self, line):
        tokens = line.split("|")
        for i, token in enumerate(tokens):
            # if not a note, skip for now
            if not re.match(r'[A-G][\-#b][0-9]', token[0:3]):
                continue
           
            # transpose Triangle down an octave
            transpose = 12 if (i == 2) else 0

            midi_pitch = self.note_str_to_int(token, transpose)
            self.midi.addNote(
                track       = i + 1, 
                channel     = i % 2, 
                start       = self.current_tick, 
                duration    = self.tick_subdivision, 
                pitch       = midi_pitch, 
                velocity    = 120
            )

    def clean_name(self, name):
        words = re.findall(r'\w+', name)
        if not words:
            return "Default"
        return "_".join([word.capitalize() for word in words])

    def run(self):
        for track in self.project.tracks:
            # reset MidiWriter
            self.midi = MidiWriter()
            
            self.current_tick = 0
            self.ticks_per_row = track.speed

            # self.midi.addBPM(track=0, start=self.current_tick, bpm=120)
            self.midi.setChannel(channel=0, program=1) 
            self.midi.setChannel(channel=1, program=1)
            
            # keep track of data for each column:
            self.col_data = [ColData() for _ in range(track.num_cols)]

            for block in track.data:
                num_lines = len(block)

                # TODO time signatures with modulo and floor
                # consider "rows_per_beat" constant, maybe defined in settings?

                for line in block:
                    self._process_line(line)
                    self.current_tick += self.tick_subdivision # 120 ticks per 16th note
            
            filename = "PROJECT_{}_TRACK_{}_{}.mid".format(
                self.clean_name(self.project.song_information.get("TITLE", "Default")),
                track.index,
                self.clean_name(track.name)
            )
            
            output_path = os.path.abspath("Exports/{}".format(filename))
            self.midi.save(output_path)
            print("[I] Midi file created @ {}".format(output_path))

        return

