# reader.py

import re

from containers.macro import Macro
#from containers.instrument import Instrument
#from containers.track import Track

# TODO handle regex not matching error

class Reader:
    def __init__(self, project):
        self.project = project
        
        self.matchers = [
            (
                re.compile(r'^\s*(TITLE|AUTHOR|COPYRIGHT|COMMENT)\s+\"(.*?)"$'),
                self.handle_song_information
            ),
            (
                re.compile(r'^\s*(MACHINE|FRAMERATE|EXPANSION|VIBRATO|SPLIT|N163CHANNELS)\s+(\d+)\s*$'),
                self.handle_global_settings
            ),
            (
                re.compile(r'^\s*(MACRO\w*)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s*:\s*((?:-?\d+\s*)+)$'),
                self.handle_macros
            )
            # TODO INSTRUMENT
            # TODO GROOVE
            # TODO DPCM
            # TODO DPCMKEY
            # TODO SPECIAL MAcros and instrument settings
            # TODO TRACK
            # TODO COLUMN
            # TODO ORDER 
            # TODO PATTERN 
            # TODO ROW
        ]
    
    def handle_song_information(self, regex_match_object):
        self.project.song_information[regex_match_object.group(1)] = regex_match_object.group(2)

    def handle_global_settings(self, regex_match_object):
        self.project.global_settings[regex_match_object.group(1)] = int(regex_match_object.group(2))

    def handle_macros(self, regex_match_object):
        # re.match(r'''
        # ^\s*               # Optional starting whitespace
        # (MACRO\w*)         # Group 1: MACRO tag (e.g., MACRO, MACRO_A)
        # \s+
        # (-?\d+)\s+         # Group 2: type
        # (-?\d+)\s+         # Group 3: index
        # (-?\d+)\s+         # Group 4: loop
        # (-?\d+)\s+         # Group 5: release
        # (-?\d+)\s*         # Group 6: setting
        # :\s*
        # ((?:-?\d+\s*)+)    # Group 7: macro sequence
        # $
        
        macro_tag = regex_match_object.group(1)
        macro_type, macro_index, macro_loop, macro_release, macro_setting = list(map(int, regex_match_object.group(2, 3, 4, 5, 6)))
        macro_sequence = list(map(int, re.findall(r'-?\d+', regex_match_object.group(7))))
        macro_key = "{}.{}.{}".format(macro_tag, macro_type, macro_index)
        macro_object = Macro(macro_tag, macro_type, macro_index, macro_loop, macro_release, macro_setting, macro_sequence)
        self.project.macros[macro_key] = macro_object
        print(macro_object)
        # TODO debug exit
        exit(0)

    def process_line(self, line: str) -> None:
        for regex_pattern, function in self.matchers:
            if x := regex_pattern.match(line):
                function(x)
            else:
                print("Unknown line: {}".format(line))
        return
    
    def read(self, input_file) -> None:
        with open(input_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line[0] == '#':
                    continue
                self.process_line(line)

