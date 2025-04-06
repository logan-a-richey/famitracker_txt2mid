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
        token = token[:3]

        if token == "---":
            return "note_off"
        if token == "===":
            return "note_release"

        matchers = [
            (r'^[A-G][\-#b][0-9]$', "note_on"),
            (r'^[0-9A-G][\-][#]$', "note_noise"),
            (r'^[\^][\-][0-4]$', "echo"),
        ]

        for pattern, event_type in matchers:
            if re.match(pattern, token):
                return event_type

        return "other"

    def handle_echo_token(self, token, col_index):
        echo_value = int(token[2])
        echo = self.echo_buffers[col_index].peek(echo_value)
        if echo:
            self.echo_buffers[col_index].push(token[3:])
            return "{}{}".format(echo, token[3:])
        
        return "...{}".format(token[3:])


    def handle_control_flow(self, data_line, orders, track):
        if re.findall(r'C[0-9A-F]{2}', data_line):
            return 'cxx_effect'

        b_matches = re.findall(r'B[0-9A-F]{2}', data_line)
        if b_matches:
            value = b_matches[-1][1:3]
            self.target_order = value if value in orders else orders[-1]
            self.target_row = 0
            return 'bxx_effect'

        d_matches = re.findall(r'D[0-9A-F]{2}', data_line)
        if d_matches:
            value = min(int(d_matches[-1][1:3], 16), track.num_rows - 1)
            self.target_order = self.get_next_item(orders, self.target_order)
            self.target_row = value
            return 'dxx_effect'

        return None

    def _parse_order_block(self, track):
        orders = list(track.orders.keys())
        order_patterns = track.orders.get(self.target_order)

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

                if token_type == 'echo':
                    token = self.handle_echo_token(token, ci)
                elif token_type in ['note_on', 'note_off', 'note_noise']:
                    self.echo_buffers[ci].push(token[:3])

                tokens.append(token)

            data_line = "|".join(tokens)
            track.data.append(data_line)

            control_result = self.handle_control_flow(data_line, orders, track)
            if control_result:
                return

        self.target_order = self.get_next_item(orders, self.target_order)
        self.target_row = 0

    def _parse_track(self, track):
        print("[I] Parsing Track {}: \'{}\'".format(track.index, track.name))
        track.data.clear()
        self.target_order = "00"
        self.target_row = 0
        self.echo_buffers = [EchoBuffer() for _ in range(track.num_cols)]

        seen_orders = set()
        while self.target_order not in seen_orders:
            seen_orders.add(self.target_order)
            self._parse_order_block(track)

        for line in track.data:
            print(line)

    def exec(self):
        for track in self.project.tracks:
            self._parse_track(track)

