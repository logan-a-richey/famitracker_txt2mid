# parser.py

import re
from typing import Dict, List, Set, Tuple, Union, Any

from containers.track import Track
# from containers.echo_buffer import EchoBuffer
from containers.track_context import TrackContext
from containers.column_context import ColumnContext
from containers.midi_data import MidiData
from containers.note_event_structs import NoteEvent, TempoEvent, TimeSigEvent

class Parser:
    ''' Contains methods for parsing tracks in a famitracker project '''
    
    # static dictionary to contain compiled regex patterns.
    regex_patterns = {
        'Bxx': re.compile(r'B[0-9A-F]{2}'),
        'Cxx': re.compile(r'C[0-9A-F]{2}'),
        'Dxx': re.compile(r'D[0-9A-F]{2}'),
        'echo_note': re.compile(r'^(?P<echo>\^\-\d)'),
        'note_on': re.compile(r'^[A-G][\-#b][0-9]'),
        'note_off': re.compile(r'^[\-]{3}'),
        'note_release': re.compile(r'^[\=]{3}'),
        'note_noise': re.compile(r'^[0-9A-F]\-#'),
        'inst': re.compile(r'^.{3}\s+(?P<inst>[0-9A-Fa-f]{2})'),
        'vol': re.compile(r'^.{3}\s+.{2}\s+(?P<vol>[0-9A-Fa-f])')
    }
    note_mapping = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

    def __init__(self, project): 
        self.project = project
       
    def classify_token(self, token: str) -> str:
        ''' Returns a string label describing the token type '''
        note_event_types = ['note_on', 'note_off', 'note_release', 'note_noise']
        for note_event_type in note_event_types:
            if Parser.regex_patterns[note_event_type].match(token):
                return note_event_type
        return "other"

    def check_to_add_echo_note(self, context: TrackContext, token: str, col: int):
        ''' 
        Checks to see if token is pushable, then push the echo token in the correct EchoBuffer. 
        We push only the first 3 characters. Only the note part is echoed. The rest of the token is preserved.
        '''
        res = self.classify_token(token)
        if res not in ['note_on', 'note_off', 'note_noise']:
            return
        context.echo_buffers[col].push(token[0:3])

    def generate_token(self, context: TrackContext, row: int, col: int) -> str:
        ''' Create a token to build up a row in `parse_order` '''
        pattern = context.patterns[col]
        token_key = "PAT={}:COL={}:ROW={}".format(pattern, col, row)
        
        null_token = "... .. .{}".format(" ..." * context.track.eff_cols[col])
        
        token = context.track.tokens.get(token_key, None)
        if not token:
            token = null_token    

        echo_match = Parser.regex_patterns['echo_note'].match(token)
        if echo_match:
            echo_value = int(echo_match.group('echo')[2])
            echo_peek = context.echo_buffers[col].peek(echo_value)
            if echo_peek:
                echo_token = "{}{}".format(echo_peek, token[3:])
                return echo_token
            
            return null_token
        
        return token

    def get_next_item(self, lst: List[str], item: str) -> str:
        ''' Given an item, get next item in a list '''

        this_index = lst.index(item)
        next_index = (this_index + 1) % len(lst)
        return lst[next_index]
    
    def get_midi_int(self, token: str) -> int:
        midi_note = Parser.note_mapping.get(token[0], 0)
        
        if token[1] == '#':
            midi_note += 1
        if token[1] == 'b':
            midi_note -= 1

        octave = int(token[2])
        midi_note = midi_note + (12*octave)

        return midi_note

    def get_noise_midi_int(self, token: str) -> int:
        return 60 + int(token[0], 16)

    def update_column_context(self, context: TrackContext, token: str, col: int):
        # update pitch
        token_type = self.classify_token(token)
        if token_type == 'note_on':
            pitch = self.get_midi_int(token[0:3])
            context.col_contexts[col].pitch = pitch
        elif token_type == 'note_noise': 
            pitch = self.get_noise_midi_int(token[0:3])
            context.col_contexts[col].pitch = pitch
        else:
            pass

        # update instrument
        inst_match = Parser.regex_patterns['inst'].match(token)
        if inst_match:
            inst_int = int(inst_match.group('inst'), 16)
            if inst_int in self.project.instruments.keys():
                context.col_contexts[col].inst = inst_int
            else:
                first_inst = list(self.project.instruments.keys())[0]
                context.col_contexts[col].inst = first_inst 
    
        # update volume
        vol_match = Parser.regex_patterns['vol'].match(token)
        if vol_match:
            vol_int = int(vol_match.group('vol'), 16)
            context.col_contexts[col].vol = vol_int

        # TODO update effects here
        pass

    def handle_control_flow(self, context: TrackContext, line: str) -> Tuple[str, int]:
        ''' 
        Handle Bxx Cxx Dxx effects. 
        Bxx: skip to order xx at row 0. if xx not in list of orders, go to last order
        Cxx: stop the song by returning the current order. target_order will be in seenit.
        Dxx: skip to next order at row xx. if xx out of range, xx = num_rows - 1
        '''

        # stop song:
        cxx_matches = Parser.regex_patterns['Cxx'].findall(line)
        if cxx_matches:
            return (context.target_order, 0)

        bxx_matches = Parser.regex_patterns['Bxx'].findall(line)
        if bxx_matches:
            last_bxx_match = bxx_matches[-1]
            bxx_value = last_bxx_match[1:]
            if bxx_value not in context.orders:
                return (context.orders[-1], 0)
            return (bxx_value, 0)

        dxx_matches = Parser.regex_patterns['Dxx'].findall(line)
        if dxx_matches:
            last_dxx_match = dxx_matches[-1]
            dxx_value = min(int(last_dxx_match[1:], 16), context.track.num_rows - 1)
            next_order = self.get_next_item(context.orders, context.target_order)
            return (next_order, dxx_value)
            
        return ()
    
    # TODO check to see if we needto create a new midi note event!
    #def poll_midi_event(self, context: TrackConext):
    #    pass

    def parse_order(self, context: TrackContext) -> int:
        ''' Parse context.target_order '''

        context.patterns = context.track.orders.get(context.target_order, None)
        if not context.patterns:
            raise ValueError("[ERROR] Could not get patterns for order {}".format(context.target_order))

        #print("Scanning Order {} -> {}".format(context.target_order, context.patterns))

        tokens = []
        for row in range(context.target_row, context.track.num_rows):
            tokens.clear()
            for col in range(context.track.num_cols):
                token = self.generate_token(context, row, col)
                tokens.append(token)
                
                self.check_to_add_echo_note(context, token, col)
                self.update_column_context(context, token, col)
                 
                # TODO 
                # fami ticks per row
                for tick in range(context.speed):
                    pass

                # TODO
                #self.poll_midi_event(context, token)
            
            # resequenced line:
            line = " | ".join(tokens)

            # handle Bxx Cxx Dxx effects
            res: Tuple[str, int] = self.handle_control_flow(context, line)
            if res:
                context.target_order, context.target_row = res
                return 0

        # end of order: go to next order
        context.target_order = self.get_next_item(context.orders, context.target_order)
        context.target_row = 0
        return 0

    def parse_track(self, track) -> int:
        ''' Parse track by recursively looping over the orders until we have read the entire track '''

        orders: List[str] = sorted(list(track.orders.keys()))
        target_order = orders[0]
        target_row = 0
        patterns: List[str] = track.orders.get(target_order)
        
        context = TrackContext(track, target_order, target_row, orders, patterns)
        seenit: Set[str] = set()
        
        while context.target_order not in seenit:
            seenit.add(context.target_order)
            self.parse_order(context)
        return 0

    def parse(self) -> int:
        ''' Parse all tracks in project '''

        for track in self.project.tracks.values():
            print("Parsing Track {} \'{}\'".format(track.index, track.name))
            self.parse_track(track)
        
        print("All tracks parsed!")
        return 0


