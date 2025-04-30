#!/usr/bin/env python3

# basic implementation of famitracker text export reader 

import re
from typing import List, Dict

class Macro:
    def __init__(self, 
        macro_type: int, 
        macro_index: int, 
        macro_loop: int, 
        macro_release: int, 
        macro_setting: int,
        macro_sequence: List[int]
    ):
        self.macro_type = macro_type
        self.macro_index = macro_index
        self.macro_loop = macro_loop
        self.macro_release = macro_release
        self.macro_setting = macro_setting
        self.macro_sequence = macro_sequence

class Instrument:
    pass

class Track:
    pass

class Project:
    def __init__(self):
        self.song_information: Dict[str, str] = {}
        self.global_settings: Dict[str, int] = {}
        self.macros: Dict[str, Macro] = {}
        self.instruments: Dict[str, Instrument] = {}
        self.tracks: List[Track] = []

class TextExportReader:
    def __init__(self, project):
        self.project = project
        self.regex_patterns = {
            "SONG_INFORMATION": re.compile(r'^\s*(\w+)\s*\"(.*)\"'),
            "GLOBAL_SETTINGS": re.compile(r'^\s*(\w+)\s*(\d+)'),
            "MACRO": re.compile(r'^\s*(\w+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s*\:\s*(.*)'),
            "DPCMDEF": re.compile(r'^\s*(\w+)\s+(\d+)\s+(\d+)\s*\"(.*)\"'),
            "DPCM": re.compile(r'^\s*(\w+)\s*\:\s*(.*)'),
            "GROOVE": re.compile(r'^\s*(\w+)\s+(\d+)\s+(\d+)\s*\:\s*(.*)'),
            "USEGROOVE": re.compile(r'^\s*(\w+)\s*\:\s*(.*)'),
            "INST2A03": re.compile(r'^\s*(\w+)(\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s*\"(.*)\"'),
            "INSTVRC6": re.compile(r'^\s*(\w+)(\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s*\"(.*)\"'),
            "INSTVRC7": re.compile(r'^\s*(\w+)\s+(\d+)\s+(\d+)\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s*\"(.*)\"'),
            "INSTFDS": re.compile(r'^\s*(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*\"(.*)\"'),
            "INSTN163": re.compile(r'^\s*(\w+)\s+(\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*\"(.*)\"'),
            "INSTS5B": re.compile(r'^\s*(\w+)(\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s*\"(.*)\"'),
            "KEYDPCM": re.compile(r'^\s*(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\-?\d+)\s+'),
            "FDSWAVE": re.compile(r'^\s*(\w+)\s+(\d+)\s*\:\s*(.*)'),
            "FDSMOD": re.compile(r'^\s*(\w+)\s+(\d+)\s*\:\s*(.*)'),
            "FDSMACRO": re.compile(r'^\s*(\w+)\s+(\d+)\s+([012])\s+(\-?\d+)\s+(\-?\d+)\s+(\d+)\s*\:\s*(.*)'),
            "N163WAVE": re.compile(r'^\s*(\w+)\s+(\d+)\s+(\d+)\s*\:\s*(.*)'),
            "TRACK": re.compile(r'^\s*(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s*\"(.*)\"'),
            "COLUMNS": re.compile(r'^\s*(\w+)\s*\:\s*(.*)'),
            "ORDER": re.compile(r'^\s*(\w+)\s+([0-9A-F]{2})\s*\:\s*(.*)'),
            "PATTERN": re.compile(r'^\s*(\w+)\s+([0-9A-F]{2})'),
            "ROW": re.compile(r'^\s*(\w+)\s+([0-9A-F]{2})\s*\:\s*(.*)'),
            "hex2d": re.compile(r'[0-9A-F]{2}'),
            "integer": re.compile(r'\-?\d+')
        }
        self.dispatch = {
            "TITLE": self._handle_song_information,
            "MACHINE": self._handle_global_settings,
            "MACRO": self._handle_macro,
            #"DPCMDEF": self._handle_dpcmdef,
            #"DPCM": self._handle_dpcm,
            #"GROOVE": self._handle_groove,
            #"USEGROOVE": self._handle_usegroove,
            #"INST2A03": self._handle_inst2a03,
            #"INSTVRC6": self._handle_instvrc6,
            #"INSTVRC7": self._handle_instvrc7,
            #"INSTFDS": self._handle_instfds,
            #"INSTN163": self._handle_instn163,
            #"INSTS5B": self._handle_insts5b,
            #"KEYDPCM": self._handle_keydpcm,
            #"FDSWAVE": self._handle_fdswave,
            #"FDSMOD": self._handle_fdsmod,
            #"FDSMACRO": self._handle_fdsmacro,
            #"N163WAVE": self._handle_n163wave,
            #"TRACK": self._handle_track,
            #"COLUMNS": self._handle_columns,
            #"ORDER": self._handle_order,
            #"PATTERN": self._handle_pattern,
            #"ROW": self._handle_row,
        }

    def _default_handler(self, line: str):
        print("Default handler: Line {}".format(line))
        return

    def _handle_song_information(self, line: str):
        regex_match = self.regex_patterns["SONG_INFORMATION"].match(line)
        if not regex_match:
            print("[W] Regex does not match! Line: ", line)
            return
        tag, name = regex_match.group(1, 2)
        self.project.song_information[tag] = name

    def _handle_global_settings(self, line: str):
        regex_match = self.regex_patterns["GLOBAL_SETTINGS"].match(line)
        if not regex_match:
            print("[W] Regex does not match! Line: ", line)
            return
        tag = regex_match.group(1)
        val = int(regex_match.group(2))
        self.project.global_settings[tag] = val
    
    def _handle_macro(self, line: str):
        regex_match: self.regex_patterns("MACRO").match(line) 
        if not regex_match:
            print("[W] Regex does not match! Line: \'{}\'".format(line))
            return
       
        macro_chip = regex_match.group(1)
        macro_type, macro_index, macro_loop, macro_release, macro_setting = list(map(
            int, 
            regex_match.group(2, 3, 4, 5, 6)
        ))
        macro_sequence = list(map(
            int,
            self.regex_patterns["integer"].findall(regex_match.group(7))
        ))
        macro_object = Macro(
            macro_type, 
            macro_index, 
            macro_loop, 
            macro_release, 
            macro_setting,
            macro_sequence
        )
        # TODO make function to generate macro_id. Perhaps hashing tuples is better
        macro_id = "{}.{}.{}".format(macro_chip, macro_type, macro_index)
        self.project.macros[macro_id] = macro_object

#    def _handle_dpcmdef(self, line: str):
#        regex_match: self.regex_patterns("DPCMDEF").match(line) 
#        if not regex_match:
#            print("[W] Regex does not match! Line: \'{}\'".format(line))
#            return
       

#   def _handle_dpcm(self, line: str):
#       regex_match: self.regex_patterns("DPCM").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_groove(self, line: str):
#       regex_match: self.regex_patterns("GROOVE").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_usegroove(self, line: str):
#       regex_match: self.regex_patterns("USEGROOVE").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_inst2a03(self, line: str):
#       regex_match: self.regex_patterns("INST2A03").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_instvrc6(self, line: str):
#       regex_match: self.regex_patterns("INSTVRC6").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_instvrc7(self, line: str):
#       regex_match: self.regex_patterns("INSTVRC7").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_instfds(self, line: str):
#       regex_match: self.regex_patterns("INSTFDS").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_instn163(self, line: str):
#       regex_match: self.regex_patterns("INSTN163").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_insts5b(self, line: str):
#       regex_match: self.regex_patterns("INSTS5B").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_keydpcm(self, line: str):
#       regex_match: self.regex_patterns("KEYDPCM").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_fdswave(self, line: str):
#       regex_match: self.regex_patterns("FDSWAVE").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_fdsmod(self, line: str):
#       regex_match: self.regex_patterns("FDSMOD").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_fdsmacro(self, line: str):
#       regex_match: self.regex_patterns("FDSMACRO").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_n163wave(self, line: str):
#       regex_match: self.regex_patterns("N163WAVE").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_track(self, line: str):
#       regex_match: self.regex_patterns("TRACK").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_columns(self, line: str):
#       regex_match: self.regex_patterns("COLUMNS").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_order(self, line: str):
#       regex_match: self.regex_patterns("ORDER").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_pattern(self, line: str):
#       regex_match: self.regex_patterns("PATTERN").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

#   def _handle_row(self, line: str):
#       regex_match: self.regex_patterns("ROW").match(line) 
#       if not regex_match:
#           print("[W] Regex does not match! Line: \'{}\'".format(line))
#           return

    def _process_line(self, line: str) -> None:
        tag = line.split()[0]
        func = self.dispatch.get(tag, self._default_handler)
        func(line)

    def read(self, input_file):
        with open(input_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line[0] == '#':
                    continue
                self._process_line(line)

if __name__ == "__main__":
    p = Project()
    r = TextExportReader(p)
    for k in r.regex_patterns.keys():
        print(k)

