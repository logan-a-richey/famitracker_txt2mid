# reader.py

import re

from containers.macro import Macro
#from containers.instrument import Instrument
#from containers.track import Track

class Reader:
    def __init__(self, project):
        self.project = project
            
    def process_line(self, line: str) -> None:
        if x := re.match(r'^\s*(TITLE|AUTHOR|COPYRIGHT|COMMENT)\s+\"(.*?)"$', line):
            self.project.song_information[x.group(1)] = x.group(2)
        
        elif x := re.match(r'^\s*(MACHINE|FRAMERATE|EXPANSION|VIBRATO|SPLIT|N163CHANNELS)\s+(\d+)\s*$', line):
            self.project.global_settings[x.group(1)] = int(x.group(2))
            #print(x.group(1), x.group(2))
        
        elif x := re.match(r'''
            ^\s*
            (MACRO\w*)         # Group 1: MACRO tag (e.g., MACRO, MACRO_A)
            \s+
            (-?\d+)\s+         # Group 2: type
            (-?\d+)\s+         # Group 3: index
            (-?\d+)\s+         # Group 4: loop
            (-?\d+)\s+         # Group 5: release
            (-?\d+)\s*         # Group 6: setting
            :\s*
            ((?:-?\d+\s*)+)    # Group 7: macro sequence
            $
        ''', line, re.VERBOSE):
            macro_tag = x.group(1)
            macro_type, macro_index, macro_loop, macro_release, macro_setting = list(map(int, x.group(2, 3, 4, 5, 6)))
            macro_sequence = list(map(int, re.findall(r'-?\d+', x.group(7))))
            macro_key = "{}.{}.{}".format(macro_tag, macro_type, macro_index)
            macro_object = Macro(macro_tag, macro_type, macro_index, macro_loop, macro_release, macro_setting, macro_sequence)
            self.project.macros[macro_key] = macro_object
            print(macro_object)
            exit()
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

