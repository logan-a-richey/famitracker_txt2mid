# parser.py

import re
import os
import logging

# Configure basic logging
#logging.basicConfig(
#    level=logging.INFO,
#    filename='app.log',
#    filemode='w',
#    format='%(asctime)s - %(levelname)s - %(message)s',
#    datefmt='%Y-%m-%d %H:%M:%S'
#)

# Log to terminal
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

from core.utils.helper_functions import generate_token_key
from submodules.midi_writer_py.midi_writer import MidiWriter

class Parser:
    def __init__(self, project):
        self.project = project
        self.midi = MidiWriter()
    
        self.track = None
        self.target_order = 0
        self.target_row = 0
        self.midi_tick = 0

        self.regex_patterns = {
            'note_on': re.compile(r'^[A-G][\-#b][0-9]'),
            # TODO : noise_on, note_off, note_release, note_echo
            'noise_on': re.compile(r'^[0-9A-F][\-][#]'),
            'bxx': re.compile(r'[B][0-9A-F]{2}'),
            'cxx': re.compile(r'[C][0-9A-F]{2}'),
            'dxx': re.compile(r'[D][0-9A-F]{2}')
        }
        self.pitch_string_to_int = {
            'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11
        }
        # define midi ticks per row
        self.midi_sub = 480 // 8

    def get_midi_pitch(self, token: str) -> int:
        midi_int = self.pitch_string_to_int.get(token[0], 0)
        if token[1] == '#':
            midi_int += 1
        octave = int(token[2]) + 1
        midi_int = midi_int + (octave * 12)
        return midi_int

    def get_next_order(self):
        orders = list(self.track.orders.keys())
        idx = orders.index(self.target_order)
        nidx = (idx + 1) % len(orders)
        return orders[nidx]
    
    def handle_control_flow(self, line: str):
        ''' Return 1 if there is an order skip. 0 if not. '''

        cxx = self.regex_patterns['cxx'].findall(line)
        if cxx:
            return 1

        bxx = self.regex_patterns['bxx'].findall(line)
        if bxx:
            self.target_row = 0

            last_match = bxx[-1]
            value = int(last_match[1:], 16)
            orders = list(self.track.orders.keys())
            if value not in orders:
                self.target_order = orders[-1]
            else:
                self.target_order = value
            return 1

        dxx = self.regex_patterns['dxx'].findall(line)
        if dxx:
            last_match = dxx[-1]
            value = min(int(last_match[1:], 16), self.track.num_rows - 1)
            self.target_row = value
            self.target_order = self.get_next_order()
            return 1

        return 0


    def parse_target_order(self):
        # print("Parsing order {}".format(self.target_order))
        # logging.info("Parsing order {}".format(self.target_order))

        if self.target_order not in self.track.orders.keys():
            raise ValueError("Target Order {} not in keys()".format(self.target_order))
        
        patterns = self.track.orders[self.target_order]
        token_row = []
        for row in range(self.target_row, self.track.num_rows):
            token_row.clear()
            for col in range(self.track.num_cols):
                token_key = generate_token_key(patterns[col], row, col)
                token = self.track.tokens.get(token_key)
                if not token:
                    continue
                
                token_row.append(token)
                
                note_match = self.regex_patterns['note_on'].match(token)
                if note_match:
                    # add the note! 
                    # self.midi.add_note(track, channel, start, dur, pitch, velocity)
                    pitch = self.get_midi_pitch(token) 
                    self.midi.add_note(col, col % 2, self.midi_tick, self.midi_sub, pitch, 120)
                
                noise_match = self.regex_patterns['noise_on'].match(token)
                if noise_match:
                    noise_pitch = int(token[0], 16) + 60
                    self.midi.add_note(col, 9, self.midi_tick, self.midi_sub, noise_pitch, 120)

            data_line = " | ".join(token_row)
            self.midi_tick += self.midi_sub
            
            res = self.handle_control_flow(data_line)
            if res:
                return
        
        self.target_order = self.get_next_order()
        self.target_row = 0
        return

    def get_output_filename(self):
        title = self.project.song_information.get("TITLE", "Project")
        index = self.track.index
        name = self.track.name

        fn = "{} Track {} {}".format(title, index, name)
        words = re.findall(r'\w+', fn)
        ofn = "_".join(word.capitalize() for word in words) + ".mid"
        return ofn

    def parse_track(self, track, output_dir):
        # init MidiWriter
        self.midi = MidiWriter()
        self.midi.add_bpm(track=0, start=0, bpm=140)
        self.midi.add_time_signature(track=0, start=0, numerator=4, denominator=4)
        # self.midi.set_channel(channel=0, program=5)
        # self.midi.set_channel(channel=1, program=6)
        self.midi.add_track_name(0, "C Major Scale")

        # reset Parser variables
        self.track = track
        self.target_order = 0

        seenit = set()
        while self.target_order not in seenit:
            seenit.add(self.target_order)
            self.parse_target_order()
       
        # Write the Midi file!
        output_filename = self.get_output_filename()
        output_path = os.path.join(output_dir, output_filename)
        self.midi.save(output_path)
        print("[INFO] The file \'{}\' has been created!".format(output_path))

    def parse(self, output_dir):
        for track in self.project.tracks:
            self.parse_track(track, output_dir)

