# parser.py

import re
from singleton import singleton
from echo_buffer import EchoBuffer

@singleton
class Parser:
    def __init__(self, project):
        self.project = project

        self.target_order = "00"
        self.target_row = 0
        self.echo_buffers = []

    def get_next_item(self, lst, item):
        item_index = lst.index(item)
        next_index = (item_index + 1) % len(lst)
        return lst[next_index]

    def determine_note_event_type(self, token):
        token = token[:3] # ensure the token is 3 characters

        if token == "---":
            return "note_off"
        
        elif token == "===":
            return "note_release" 
        
        elif re.match(r'[A-G][\-#b][0-9]', token):
            return "note_on"
        
        elif re.match(r'[0-9A-G][\-][#]', token):
            return "note_noise"
        
        elif re.match(r'[\^][\-][0-4]', token):
            return "echo"
        
        return "other"

    def _parse_track_order(self, track):
        orders = list(track.orders.keys())
        patterns = list(track.patterns.keys())

        #print("Scanning Order: {}".format(self.target_order))
        order_patterns = track.orders.get(self.target_order)

        #print("{} -> {}".format(self.target_order, order_patterns))
        
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
                
                token_type = self.determine_note_event_type(token)
                
                # Handle echo notes
                if token_type == 'echo':
                    echo_value = int(token[2])
                    echo = self.echo_buffers[ci].peek(echo_value)
                    if echo:
                        token = "{}{}".format(echo, token[3:])
                        self.echo_buffers[ci].push(token[3:])
                    else:
                        token = "...{}".format(token[3:])
                
                if token_type in ['note_on', 'note_off', 'noise_on']:
                    self.echo_buffers[ci].push(token[0:3])

                tokens.append(token)
            
            data_line = "|".join(tokens)
            track.data.append(data_line)

            # TODO
            all_matches = re.findall(r'[BCD][0-9A-F]{2}', data_line)
            if all_matches:
                print(all_matches)

            matches = re.findall(r'[C][0-9A-F]{2}', data_line)
            if matches:
                return # end the track. current order is in seenit

            matches = re.findall(r'[B][0-9A-F]{2}', data_line)
            if matches:
                # get the value of the last match
                value = matches[-1][1:3]
                if value not in orders:
                    self.target_order = orders[-1]
                    self.target_row = 0
                    return
                
                self.target_order = value
                self.target_row = 0
                return

            matches = re.findall(r'[D][0-9A-F]{2}', data_line)
            if matches:
                # get the value of the last match and convert from int to hex
                # then bounds check with (num_rows - 1)
                value = min(int(matches[-1][1:3], 16), track.num_rows - 1)
                
                # get next order         
                self.target_order = self.get_next_item(orders, self.target_order)
                self.target_row = value
                return

        # get next order
        self.target_order = self.get_next_item(orders, self.target_order)
        self.target_row = 0
        return

    def _parse_track(self, track):
        print("Parsing TRACK {} \'{}\'".format( track.index, track.name))
        
        track.data.clear()
        self.target_order = "00"
        self.target_row = 0
        
        self.echo_buffers.clear()
        self.echo_buffers = [EchoBuffer() for _ in range(track.num_cols)]

        seen_it = set()

        while (self.target_order not in seen_it):
            seen_it.add(self.target_order)
            self._parse_track_order(track)

    def exec(self):
        # Adds self.resequenced_rows to each track in preparation for the MIDI export.
        for track in self.project.tracks:
            self._parse_track(track)
        pass

