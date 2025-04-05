# parser.py

import re
from singleton import singleton

@singleton
class Parser:
    def __init__(self, project):
        self.project = project

        self.target_order = "00"
        self.target_row = 0

    def get_next_item(self, lst, item):
        item_index = lst.index(item)
        next_index = (item_index + 1) % len(lst)
        return lst[next_index]

    def _parse_track_order(self, track):
        orders = list(track.orders.keys())
        patterns = list(track.patterns.keys())

        #print("Scanning Order: {}".format(self.target_order))
        order_patterns = track.orders.get(self.target_order)

        print("{} -> {}".format(self.target_order, order_patterns))
        
        tokens = []
        for ri in range(self.target_row, track.num_rows):
            tokens.clear()
            for ci in range(track.num_cols):
                # TODO
                #for tick in range(self.num_ticks):
                null_token = "... .. .{}".format(" ..."*track.eff_cols[ci])
                lookup = track.patterns.get(order_patterns[ci], {}).get(ri, None)
                
                if not lookup:
                    tokens.append(null_token)
                    continue
                token = lookup[ci]
                
                tokens.append(token)
            print(tokens) 
            exit()

        self.target_order = self.get_next_item(orders, self.target_order)
        return

    def _parse_track(self, track):
        print("Parsing TRACK {} \'{}\'".format( track.index, track.name))
        
        self.target_order = "00"
        seen_it = set()
        while (self.target_order not in seen_it):
            seen_it.add(self.target_order)
            self._parse_track_order(track)
        
    def exec(self):
        ''' 
        Adds self.resequenced_rows to each track in preparation for the MIDI export.
        '''
        for track in self.project.tracks:
            self._parse_track(track)
        pass

