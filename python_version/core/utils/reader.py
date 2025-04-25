# reader.py

import re
import logging
logging.basicConfig(level=logging.ERROR)

from typing import Dict, Callable

from core.containers.track import Track
from core.utils.helper_functions import generate_token_key

class Reader:
    def __init__(self, project):
        self.project = project
        
        self.regex_patterns = {
            "SONG_INFORMATION": re.compile(r"""
                ^(?P<tag>\w+)\s+
                \"(?P<val>.*)\"
            """, re.VERBOSE),
            "GLOBAL_SETTINGS": re.compile(r"""
                ^(?P<tag>\w+)\s+
                (?P<val>\d+)
            """, re.VERBOSE),
            # TRACK 64 6 150 "title"
            "TRACK": re.compile(r"""
                ^(?P<tag>\w+)\s+
                (?P<num_rows>\d+)\s+
                (?P<speed>\d+)\s+
                (?P<tempo>\d+)\s*\"
                (?P<name>.*)\"
            """, re.VERBOSE),
            "COLUMNS": re.compile(r"""
                ^(?P<tag>\w+)
                \s*\:\s*
                (?P<data>.*)
            """, re.VERBOSE),
            "ORDER": re.compile(r"""
                ^(?P<tag>\w+)\s+
                (?P<order_id>[0-9A-F]{2})
                \s*\:\s*
                (?P<data>.*)
            """, re.VERBOSE),
            "PATTERN": re.compile(r"""
                ^(?P<tag>\w+)\s+
                (?P<pattern_id>[0-9A-F]{2})
            """, re.VERBOSE),
            "ROW": re.compile(r"""
                ^(?P<tag>\w+)\s+
                (?P<row_id>[0-9A-F]{2})
                \s*\:\s*
                (?P<data>.*)
            """, re.VERBOSE),
            "no_colon": re.compile(r"([^:])"),
            "2d_hex": re.compile(r"([0-9A-F]{2})"),
            "integer": re.compile(r"(\-?\d+)"),
            "blank_token": re.compile(r"^[\.\s]+$")
        }
        self.handlers: Dict[str, Callable[[str], None]] = {
            **{key: self.handle_song_information for key in [
                "TITLE","AUTHOR","COPYRIGHT","COMMENT"]},
            **{key: self.handle_global_settings for key in [
                "MACHINE","FRAMERATE","EXPANSION","VIBRATO","SPLIT","N163CHANNELS"]},
            "TRACK"         : self.handle_track,
            "COLUMNS"       : self.handle_columns,
            "ORDER"         : self.handle_order,
            "PATTERN"       : self.handle_pattern,
            "ROW"           : self.handle_row,
        }
        self.target_pattern: int = 0
    
    def handle_song_information(self, line):
        my_match = self.regex_patterns["SONG_INFORMATION"].match(line)
        if not my_match:
            raise ValueError("Regex failed to match. Line: \'{}\'".format(line))

        key, val = my_match.group("tag", "val")
        self.project.song_information[key] = val

    def handle_global_settings(self, line):
        my_match = self.regex_patterns["GLOBAL_SETTINGS"].match(line)
        if not my_match:
            raise ValueError("Regex failed to match. Line: \'{}\'".format(line))
        
        key = my_match.group("tag")
        val = int(my_match.group("val"))
        self.project.global_settings[key] = val
    
    def handle_track(self, line):
        my_match = self.regex_patterns["TRACK"].match(line)
        if not my_match:
            raise ValueError("Regex failed to match. Line: \'{}\'".format(line))

        num_rows, speed, tempo = list(map(int, my_match.group("num_rows", "speed", "tempo")))
        name = my_match.group("name")

        track = Track(num_rows, speed, tempo, name)
        self.project.tracks.append(track)
    
    def handle_columns(self, line):
        if not self.project.tracks:
            raise ValueError("Track not initialized yet. Line: \'{}\'".format(line))
        
        target_track = self.project.tracks[-1]
        
        my_match = self.regex_patterns["COLUMNS"].match(line)
        if not my_match:
            raise ValueError("Regex failed to match. Line: \'{}\'".format(line))

        eff_cols = list(map(int, self.regex_patterns["integer"].findall(my_match.group("data"))))
        num_cols = len(eff_cols)

        target_track.num_cols = num_cols
        target_track.eff_cols = eff_cols
    
    def handle_order(self, line):
        if not self.project.tracks:
            raise ValueError("Track not initialized yet. Line: \'{}\'".format(line))
        
        target_track = self.project.tracks[-1]

        my_match = self.regex_patterns["ORDER"].match(line)
        if not my_match:
            raise ValueError("Regex failed to match. Line: \'{}\'".format(line))

        order_id = int(my_match.group("order_id"), 16)
        patterns = [int(pattern, 16) for pattern in self.regex_patterns["2d_hex"].findall(my_match.group("data"))]

        if len(patterns) != target_track.num_cols:
            raise ValueError("num_patterns != num_cols | Line: \'{}\'".format(line))

        target_track.orders[order_id] = patterns
    
    def handle_pattern(self, line):
        if not self.project.tracks:
            raise ValueError("Track not initialized yet. Line: \'{}\'".format(line))
        
        target_track = self.project.tracks[-1]
  
        my_match = self.regex_patterns["PATTERN"].match(line)
        if not my_match:
            raise ValueError("Regex failed to match. Line: \'{}\'".format(line))

        self.target_pattern = int(my_match.group("pattern_id"), 16)
    
    def handle_row(self, line):
        if not self.project.tracks:
            raise ValueError("Track not initialized yet. Line: \'{}\'".format(line))
        
        target_track = self.project.tracks[-1]

        my_match = self.regex_patterns["ROW"].match(line)
        if not my_match:
            raise ValueError("Regex failed to match. Line: \'{}\'".format(line))
        
        row_int = int(my_match.group("row_id") , 16)
        tokens = [token.strip() for token in my_match.group("data").split(":")]

        if len(tokens) != target_track.num_cols:
            raise ValueError("num_tokens != num_cols | Line: \'{}\'".format(line))

        for col, token in enumerate(tokens):
            if (is_blank_token := self.regex_patterns["blank_token"].match(token)):
                continue

            token_key = generate_token_key(self.target_pattern, row_int, col) 
            target_track.tokens[token_key] = token
            # token = [PITCH] [INST] [VOL] [FX1-4] [FXPARAM1-4]
            # PITCH: NOTE_ON = [0: 127]
            # PITCH: NOTE_NULL = -1
            # PTICH: NOTE_OFF = -2
            # PITCH: NOTE_REL = -3
            # INST = [0:64]
            # VOL = [0 : 15]
            # (ascii = 1 byte = 8 bit 0000 0000) 
            # fx_1 = 4 bytes = 32 bits? 
            # fx_p = 0x``47

    def process_line(self, line):
        first_word = line.split()[0]
        func = self.handlers.get(first_word, None)
        if not func:
            return

        try:
            func(line)
        except Exception as e:
            logging.error(e)
            exit(1)

    def read(self, input_file):
        with open(input_file, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line[0] == "#":
                    continue
                self.process_line(line)

