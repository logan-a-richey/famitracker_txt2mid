# parser.py

import re
from typing import List, Dict, Set, Tuple, Union
#from utils.singleton import SingletonMeta

from containers.track import Track

class Parser:
    regex_patterns = {
        # global effects
        "bxx" : re.compile(r'[B][0-9A-F]{2}'), # order skip to xx
        "cxx" : re.compile(r'[B][0-9A-F]{2}'), # order skip stop song
        "dxx" : re.compile(r'[B][0-9A-F]{2}'), # order skip next order at row xx
        "bcd_xx": re.compile(r'[BCD][0-9A-F]{2}'), # detect any order skip effect
        "fxx" : re.compile(r'[F][0-9A-F]{2}'), # speed xx, if xx < SPLIT speed change, else tempo change
        "oxx" : re.compile(r'[O][0-9A-F]{2}'), # groove xx
        # column effects
        "qxx" : re.compile(r'[Q][0-9A-F]{2}'), # pitch bend up
        "rxx" : re.compile(r'[R][0-9A-F]{2}'), # pitch bend down
        "gxx" : re.compile(r'[G][0-9A-F]{2}'), # note delay start, xx fami ticks
        "sxx" : re.compile(r'[S][0-9A-F]{2}'), # note delay stop, xx fami ticks
        "0xx" : re.compile(r'[0][0-9A-F]{2}')  # arpeggio effect
    }
    
    def __init__(self, project):
        self.project = project

    def get_next_order(self, track: Track, current_order: str) -> str:
        list_orders = list(track.orders.keys())
        #print("list_orders", list_orders)
        current_index = list_orders.index(current_order)
        next_index = (current_index + 1) % len(list_orders)
        next_order = list_orders[next_index]
        return next_order

    def handle_control_flow(self,
        track: Track, 
        target_order: str, 
        data_line: str
    ) -> Tuple[str, int]:
        ''' Handle order skipping effects Bxx Cxx Dxx '''
        list_orders = list(track.orders.keys())

        any_match = Parser.regex_patterns['bcd_xx'].findall(data_line)
        if any_match:
            print("Found order skip matches! {}".format(any_match))

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
            
            dxx_value = int(last_match[1:], 16)
            dxx_value = min(dxx_value, track.num_rows - 1)

            next_order = self.get_next_order(track, target_order)
            return (next_order, dxx_value)

        return () # return empty set (should return false) # TODO

    def generate_token(self, track: Track, list_patterns: List[str], ci: int, ri: int) -> str:
        token_key = "PAT={}:COL={}:ROW={}".format(list_patterns[ci], ci, ri)
        token: Union[str, None] = track.tokens.get(token_key, None)
        if not token:
            token = "... .. .{}".format(' ...' * track.eff_cols[ci])
        return token

    def parse_order(self, track: Track, target_order: str, target_row: int) -> Tuple[str, int]:
        # check to see if key exists
        if not target_order in list(track.orders.keys()):
            print("[E] Target order {} is not in track.orders.keys()".format(target_order))
            exit(1)

        # check to see if value exists
        list_patterns = track.orders.get(target_order, None)
        if not list_patterns:
            print("Could not get track.orders[{}]".format(target_order))
            exit(1)
        
        print("Scanning: {} -> {}".format(target_order, track.orders.get(target_order)))

        list_tokens = []
        for ri in range(target_row, track.num_rows):
            list_tokens.clear()
            for ci in range(track.num_cols):
                # TODO handle macros:w
                #for ti in range(track.speed):
                #    pass
                token = self.generate_token(track, list_patterns, ci, ri)
                
                #print("Found! {}".format(token_key))
                list_tokens.append(token)

                pass
            data_row = " | ".join(list_tokens)
            print(data_row)
            
            # TODO handle Order Skipping effects 
            res = self.handle_control_flow(track, target_order, data_row)
            if res:
                next_order = res[0]
                next_row = res[1]
                return (next_order, next_row)
            
            continue
        
        next_order = self.get_next_order(track, target_order)
        next_row = 0
        return (next_order, next_row)

    def parse_track(self, track: Track) -> int:
        # target_order = list(track.orders.keys())[0]
        target_order =  "00"
        target_row = 0

        seen_it: Set[str] = set()
        while (target_order not in seen_it):
            seen_it.add(target_order)
            target_order, target_row = self.parse_order(track, target_order, target_row)
        return 0

    def parse(self) -> int:
        ''' Prepare data for MIDI reading '''
        for track in self.project.tracks.values():
            self.parse_track(track)
        return 0

