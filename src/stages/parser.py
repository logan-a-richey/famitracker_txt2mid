# parser.py

import re
from typing import List, Dict, Set, Tuple, Union, Any
#from utils.singleton import SingletonMeta

from containers.track import Track

# TODO mutliprocessing to handle multiple tracks at once?
class Parser:
    ''' Contains methods for parsing tracks in a famitracker Project '''

    # static dictionary for compiled regex lookups
    regex_patterns: Dict[str, Any] = {
        # global effects
        "bxx" : re.compile(r'B[0-9A-F]{2}'), # order skip to xx
        "cxx" : re.compile(r'C[0-9A-F]{2}'), # order skip stop song
        "dxx" : re.compile(r'D[0-9A-F]{2}'), # order skip next order at row xx
        "bcd_xx": re.compile(r'[BCD][0-9A-F]{2}'), # detect any order skip effect
        "fxx" : re.compile(r'F[0-9A-F]{2}'), # speed xx, if xx < SPLIT speed change, else tempo change
        "oxx" : re.compile(r'O[0-9A-F]{2}'), # groove xx
        # column effects
        "qxx" : re.compile(r'Q[0-9A-F]{2}'), # pitch bend up
        "rxx" : re.compile(r'R[0-9A-F]{2}'), # pitch bend down
        "gxx" : re.compile(r'G[0-9A-F]{2}'), # note delay start, xx fami ticks
        "sxx" : re.compile(r'S[0-9A-F]{2}'), # note delay stop, xx fami ticks
        "0xx" : re.compile(r'0[0-9A-F]{2}')  # arpeggio effect
    }
     
    def __init__(self, project):
        ''' Class constructor. Set a reference back to parent Project class '''
        self.project = project

    def get_next_order(self, track: Track, current_order: str) -> str:
        ''' Returns the next item of a list (with wrap around) '''
        list_orders = list(track.orders.keys())
        if current_order not in list_orders:
            print("[E] Index error. Tried to find {} in list {}".format(current_order, list_orders))
            exit(1)

        #print("list_orders", list_orders)
        current_index = list_orders.index(current_order)
        next_index = (current_index + 1) % len(list_orders)
        next_order = list_orders[next_index]
        return next_order

    def handle_control_flow(self, track: Track, target_order: str, data_line: str) -> Tuple[str, int]:
        ''' Handle order skipping effects Bxx Cxx Dxx '''
        list_orders = list(track.orders.keys())

#        any_match = Parser.regex_patterns['bcd_xx'].findall(data_line)
#        if any_match:
#            print("Found order skip matches! {}".format(any_match))
#            pass

        cxx_matches = Parser.regex_patterns['cxx'].findall(data_line)
        if cxx_matches:
            # return the current target_order to end the song (already in seen_it)
            return (target_order, 0)
       
        # go to order xx, if xx not in list of orders, to to last order
        bxx_matches = Parser.regex_patterns['bxx'].findall(data_line)
        if bxx_matches:
            last_match = bxx_matches[-1]
            bxx_value = last_match[1:]
            if bxx_value not in list_orders:
                bxx_value = list_orders[-1]
            return (bxx_value, 0)

        # go to next order at row xx, if xx out of bounds, go to last row of next order
        dxx_matches = Parser.regex_patterns['dxx'].findall(data_line)
        if dxx_matches:
            last_match = dxx_matches[-1]
            next_order = self.get_next_order(track, target_order)
            dxx_value = min(int(last_match[1:], 16), track.num_rows - 1)
            return (next_order, dxx_value)

        return None
    
    # TODO
    #def handle_speed_and_tempo(self):

    def generate_token(self, track: Track, list_patterns: List[str], ci: int, ri: int) -> str:
        ''' Generates token based on pattern/order lookup. Used in `self.parse_order()` '''
        token_key = "PAT={}:COL={}:ROW={}".format(list_patterns[ci], ci, ri)
        token: Union[str, None] = track.tokens.get(token_key, None)
        if not token:
            token = "... .. .{}".format(' ...' * track.eff_cols[ci])
        return token

    def parse_order(self, track: Track, target_order: str, target_row: int) -> Tuple[str, int]:
        ''' Parses a single order from a track '''
        # check to see if key exists
        if not target_order in list(track.orders.keys()):
            print("[E] Target order {} is not in track.orders.keys()".format(target_order))
            exit(1)

        # check to see if value exists
        list_patterns = track.orders.get(target_order, None)
        if not list_patterns:
            print("[E] Could not get track.orders[{}]".format(target_order))
            exit(1)
        
        print("Scanning: {} -> {}".format(target_order, track.orders.get(target_order)))

        list_tokens: List[str] = []
        for ri in range(target_row, track.num_rows):
            list_tokens.clear()
            for ci in range(track.num_cols):
                token = self.generate_token(track, list_patterns, ci, ri)
                list_tokens.append(token)
                # TODO handle macros:w
                #for ti in range(track.speed):
                #    pass
                pass
            
            data_line = " | ".join(list_tokens)
            track.data_lines.append(data_line)
            
            # handle order skipping effects
            res: Union[Set[str, int], None] = self.handle_control_flow(track, target_order, data_line)
            if res:
                return res
            continue
        
        next_order = self.get_next_order(track, target_order)
        next_row = 0
        return (next_order, next_row)

    def parse_track(self, track: Track) -> int:
        ''' Recursively parse the orders until we have read the entire Track '''
        # target_order = list(track.orders.keys())[0]
        track.data_lines.clear()
        target_order =  "00"
        target_row = 0

        seen_it: Set[str] = set()
        while (target_order not in seen_it):
            seen_it.add(target_order)
            target_order, target_row = self.parse_order(track, target_order, target_row)
        
        #for line in track.data_lines:
        #    print(line)

        return 0

    def parse(self) -> int:
        ''' Loop over all Tracks in Project and prepare data for MIDI reading '''
        for track in self.project.tracks.values():
            self.parse_track(track)
        return 0

