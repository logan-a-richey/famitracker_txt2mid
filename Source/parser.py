# parser.py

import re
import os
import logging

from typing import List, Dict, Any

from singleton import singleton
from echo_buffer import EchoBuffer

TICKS_PER_ROW = 120

def int_to_hex(value: int) -> str:
    if not (0 <= value <= 255):
        raise ValueError("Input must be an integer between 0 and 255.")
    return f"0x{value:02X}"

@singleton
class Parser:
    def __init__(self, project):
        self.project = project
        
        # running track of variables
        self.target_order: str = "00"
        self.target_row: int = 0
        self.speed: int = 6
        self.midi_tick: int = 0

        # keep track of each row's echo data
        self.echo_buffers: List[EchoBuffer] = []
        
        # max number of lines to print for each patterns (for logging)
        self.head_patterns: int = 10

        self.regex_patterns = {
            "note_on"      : re.compile(r'^[A-G][\-#b][0-9]$'),
            "note_noise"   : re.compile(r'^[0-9A-G][\-][#]$'),
            "note_echo"    : re.compile(r'^[\^][\-][0-4]$'),
            "note_off"     : re.compile(r'^[\-]{3}$'),
            "note_release" : re.compile(r'^[\=]{3}$'),

            "bxx_effect"   : re.compile(r'[B][0-9A-F]{2}'), # skip: go to order xx
            "cxx_effect"   : re.compile(r'[C][0-9A-F]{2}'), # skip: end song
            "dxx_effect"   : re.compile(r'[D][0-9A-F]{2}'), # skip: next order at row xx
            
            "fxx_effect"   : re.compile(r'[F][0-9A-F]{2}'), # speed effect
            "oxx_effect"   : re.compile(r'[O][0-9A-F]{2}'), # groove effect
            
            "rxx_effect"   : re.compile(r'[R][0-9A-F]{2}'), # note pitch down effect
            "qxx_effect"   : re.compile(r'[Q][0-9A-F]{2}'), # note pitch up effect
            "0xx_effect"   : re.compile(r'[0][0-9A-F]{2}'), # arpeggio effect
            "gxx_effect"   : re.compile(r'[G][0-9A-F]{2}'), # note start delay effect
            "sxx_effect"   : re.compile(r'[S][0-9A-F]{2}')  # note cut delay effect
        }

        self.note_mapping = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    
    def get_next_item(self, lst: List[Any], item: Any):
        # returns next item of a list
        item_index = lst.index(item)
        next_index = (item_index + 1) % len(lst)
        return lst[next_index]

    def determine_note_event_type(self, token):
        token = token[:3]
        note_types = ["note_on", "note_off", "note_release", "note_noise", "note_echo"]
        for n in note_types:
            if n in self.regex_patterns:
                if self.regex_patterns[n].match(token):
                    return n
        return "other"

    def handle_echo_token(self, token, col_index):
        echo_value = int(token[2])
        echo = self.echo_buffers[col_index].peek(echo_value)
        if echo:
            self.echo_buffers[col_index].push(token[3:])
            return "{}{}".format(echo, token[3:])
        
        return "...{}".format(token[3:])
    
    def note_str_to_int(self, token, transpose=0):
        if not self.regex_patterns["note_on"].match(token[0:3]):
            print("[E] Bad note format: {}".format(token))
            #return None

        note_int = self.note_mapping.get(token[0], 0)
        accidental = token[1]
        octave = int(token[2]) + 1

        midi_int = (octave * 12) + note_int + transpose
        midi_int = (midi_int + 1) if (accidental == "#") \
            else (midi_int - 1) if (accidental == "b") \
            else midi_int
        
        return midi_int

    def handle_control_flow(self, data_line, orders, track):
        if self.regex_patterns["cxx_effect"].findall(data_line):
            return 'cxx_effect'

        b_matches = self.regex_patterns["bxx_effect"].findall(data_line)
        if b_matches:
            value = b_matches[-1][1:3]
            self.target_order = value if value in orders else orders[-1]
            self.target_row = 0
            return 'bxx_effect'

        d_matches = self.regex_patterns["dxx_effect"].findall(data_line)
        if d_matches:
            value = min(int(d_matches[-1][1:3], 16), track.num_rows - 1)
            self.target_order = self.get_next_item(orders, self.target_order)
            self.target_row = value
            return 'dxx_effect'

        return None
     
    def _handle_fxx_effect(self, value):
        if value > self.project.global_settings.get("SPLIT", 32):
            # update speed (famitracker ticks per row)
            self.speed = value
        else:
            # TODO update BPM
            pass

    def _handle_oxx_effect(self, value):
        # TODO handle groove effect (loop famitracker speeds per row through groove seq)
        pass

    def _handle_speed_matches(self, line):
        # look for speed effects
        speed_matches = re.findall(r'[FO][0-9A-F]{2}', line)
        if not speed_matches:
            return

        last_match = speed_matches[-1]
        #print("[D] Found speed match! {}".format(last_match))

        match_type = last_match[0]
        match_value = int(last_match[1:3], 16)

        # speed setting
        if match_type == "F":
            self._handle_fxx_effect(match_value)
        # groove setting
        elif match_type == "O":
            self.handle_oxx_effect(match_value)
        else:
            pass


    def get_midi_tokens(self, tokens) -> List[List[str]]:
        midi_tokens = []
        for token in tokens:
            temp = []
            part_note, part_inst, part_vol = token.split()[0:3]
            # note part
            if self.regex_patterns["note_on"].match(part_note):
                temp.append(str(self.note_str_to_int(part_note)))
            else:
                temp.append("NULL")
            # inst part
            if re.match(r'^[0-9A-F]{2}$', part_inst):
                temp.append(str(int(part_inst, 16)))
            else:
                temp.append("NULL")
            # vol part
            if re.match(r'^[0-9A-F]$', part_vol):
                temp.append(str(int(part_vol, 16)))
            else:
                temp.append("NULL")
            #print("TOKEN = {} | PARTS = {}".format(token.ljust(20), temp))
            midi_tokens.append(temp)
        return midi_tokens
    
    def _parse_order_block(self, track):
        orders = list(track.orders.keys())
        order_patterns = track.orders.get(self.target_order)
       
        # TODO 
        # append a new order block
        #track.data.append([])
        #this_block = track.data[-1]

        for ri in range(self.target_row, track.num_rows):
            tokens = []
            for ci in range(track.num_cols):
                null_token = "... .. .{}".format(" ..." * track.eff_cols[ci])
                pattern_data = track.patterns.get(order_patterns[ci], {}).get(ri, None)

                if not pattern_data:
                    tokens.append(null_token)
                    continue

                token = pattern_data[ci]
                token_type = self.determine_note_event_type(token)

                if token_type == 'note_echo':
                    token = self.handle_echo_token(token, ci)
                elif token_type in ['note_on', 'note_off', 'note_noise']:
                    self.echo_buffers[ci].push(token[:3])

                tokens.append(token)
            
            data_line = " : ".join(tokens)
            self._handle_speed_matches(data_line)
            
            midi_tokens: List[List[str]] = self.get_midi_tokens(tokens)

            # midi data row 
            mdr = []
            mdr.append("{}".format(str(self.midi_tick).rjust(10)))
            mdr.append("{}".format(int_to_hex(self.speed)))

            for t in midi_tokens:
                mdt  = []
                for v in t:
                    if v == 'NULL':
                        mdt.append(v)
                        continue
                    mdt.append(int_to_hex(int(v)))
                mdr.append(" ".join(mdt))

            print(" : ".join(mdr))

            # TODO
            #exit()

            self.midi_tick += TICKS_PER_ROW

            control_result = self.handle_control_flow(data_line, orders, track)
            if control_result:
                return

        self.target_order = self.get_next_item(orders, self.target_order)
        self.target_row = 0

        # TODO debug exit
        #exit()

    def _parse_track(self, track):
        
        # TODO logger
        print("[I] Parsing Track {}: \'{}\'".format(track.index, track.name))
        
        #track.data.clear()
        self.target_order = "00"
        self.target_row = 0
        self.echo_buffers = [EchoBuffer() for _ in range(track.num_cols)]
        
        self.midi_tick = 0

        seen_orders = set()
        while self.target_order not in seen_orders:
            seen_orders.add(self.target_order)
            self._parse_order_block(track)

    def run(self):
        for track in self.project.tracks:
            self._parse_track(track)
        
        # TODO debug exit
        exit(0)


