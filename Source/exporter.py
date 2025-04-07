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
        self.ticks_per_row = 6
        
    def note_str_to_int(self, token, transpose=0):
        if not re.match(r'[A-G][\-b#][0-9]', token[0:3]):
            print("[E] Bad note format: {}".format(token))
            exit(1)

        note_int = self.note_mapping.get(token[0], 0)
        accidental = token[1]
        octave = int(token[2]) + 1

        midi_int = (octave * 12) + note_int + transpose
        midi_int = (midi_int + 1) if (accidental == "#") \
            else (midi_int - 1) if (accidental == "b") \
            else midi_int
        
        return midi_int

    def _handle_fxx_effect(self, value):
        pass

    def _handle_oxx_effect(self, value):
        pass

    def _handle_speed_matches(self, line):
        # look for speed effects
        speed_matches = re.findall(r'[FO][0-9A-F]{2}', line)
        if not speed_matches:
            return

        last_match = speed_matches[-1]
        speed_type = last_match[0]
        value = int(last_match[1:3], 16)

        # speed setting
        if speed_type == "F":
            self._handle_fxx_effect(value)
        # groove setting
        elif speed_type == "O":
            self.handle_oxx_effect(value)
        else:
            pass
        
        return

    def determine_note_event_type(self, token):
        # look at first 3 characters (note part)
        token = token[:3]

        if token == "---":
            return "note_off"
        if token == "===":
            return "note_release"

        matchers = [
            (r'^[A-G][\-#b][0-9]$', "note_on"),
            (r'^[0-9A-G][\-][#]$', "note_noise"),
            #(r'^[\^][\-][0-4]$', "echo"),
        ]

        for pattern, event_type in matchers:
            if re.match(pattern, token):
                return event_type

        return "other"
    
    def _process_note_on(self, col_index: int, token: str):
        # transpose Triangle down an octave
        
        transpose = 12 if (col_index == 2) else 0
        
        midi_pitch = self.note_str_to_int(token, transpose)
        self.midi.addNote(
            track       = col_index, 
            channel     = col_index % 2, 
            start       = self.current_tick, 
            duration    = self.tick_subdivision, 
            pitch       = midi_pitch, 
            velocity    = 120
        )
        return

    def _process_note_off(self, token):
        pass

    def _process_note_release(self, token):
        pass

    def _process_note_noise(self, token):
        pass

    def _process_line(self, line):
        tokens = line.split("|")
        for col_index, token in enumerate(tokens):
            self._handle_speed_matches(line)
            
            # capture the note part
            #note_part, inst_part, vol_part = line.split()[0:3]
            #effects = line.split()[3:]
            
            note_event_type = self.determine_note_event_type(token)

            if note_event_type == "note_on":
                self._process_note_on(col_index, token)
            elif note_event_type == "note_off":
                self._process_note_off(token)
            elif note_event_type == "note_release":
                self._process_note_release(token)
            elif note_event_type == "note_noise":
                self._process_note_noise(token)
            
        return


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

