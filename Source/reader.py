# reader.py

import re

from macro import Macro
# from dpcm import DPCM
# from groove import Groove
# from instrument import *
# from track import Track

class Reader:
    def __init__(self, project):
        self.project = project
        self.dispatch_table = {
            "TITLE": self._handle_song_information,
            "AUTHOR": self._handle_song_information,
            "COPYRIGHT": self._handle_song_information,
            "COMMENT": self._handle_song_information,
            
            "MACHINE": self._handle_global_settings,
            "FRAMERATE": self._handle_global_settings,
            "EXPANSION": self._handle_global_settings,
            "VIBRATO": self._handle_global_settings,
            "SPLIT": self._handle_global_settings,
            "N163CHANNELS": self._handle_global_settings,

            "MACRO": self._handle_macro,
            "MACROVRC6": self._handle_macrovrc6,
            "MACRON163": self._handle_macron163,
            "MACROS5B": self._handle_macros5b,
            
            "DPCMDEF": self._handle_dpcmdef,
            "DPCM": self._handle_dpcm,
            "GROOVE": self._handle_groove,
            "USEGROOVE": self._handle_usegroove,
            
            "INST2A03": self._handle_inst2a03,
            "INSTVRC6": self._handle_instvrc6,
            "INSTVRC7": self._handle_instvrc7,
            "INSTFDS": self._handle_instfds,
            "INSTN163": self._handle_instn163,
            "INSTS5B": self._handle_insts5b,
            
            "KEYDPCM": self._handle_keydpcm,
            "FDSWAVE": self._handle_fdswave,
            "FDSMOD": self._handle_fdsmod,
            "FDSMACRO": self._handle_fdsmacro,
            "N163WAVE": self._handle_n163wave,
            
            "TRACK": self._handle_track,
            "COLUMNS": self._handle_columns,
            "ORDER": self._handle_order,
            "PATTERN": self._handle_pattern,
            "ROW": self._handle_row
        }

    def get_quote(self, s):
        # return text between first and last double quote
        return s[s.find("\"") + 1: s.rfind("\"")]

    def _nop(self, line):
        pass

    def _handle_song_information(self, line):
        k = line.split()[0]
        v = self.get_quote(line)
        self.project.song_information[k] = v

    def _handle_global_settings(self, line):
        k = line.split()[0]
        v = int(line.split()[-1])
        self.project.global_settings[k] = v

    def _handle_macro(self, line, chip="blank"):
        m_chip = chip
        m_type, m_index, m_loop, m_release, m_setting = map(int, line.split()[1:6])
        m_seq = map(int, line.split(":")[1].strip().split())

        m_macro = Macro(
            m_chip, m_type, m_index, m_loop, m_release, m_setting, m_seq
        )
        m_key = "{}.{}.{}".format(m_chip, m_type, m_index)

        self.project.macros[m_key] = m_macro

    def _handle_macrovrc6(self, line):
        self._handle_macro(line, chip="vrc6")

    def _handle_macron163(self, line):
        self._handle_macro(line, chip="n163")

    def _handle_macros5b(self, line):
        self._handle_macro(line, chip="s5b")

    def _handle_dpcmdef(self, line):
        m_index, m_size = map(int, line.split()[1:3])
        m_name = self.get_quote(line)
        m_dpcm = DPCM(m_index, m_size, m_name)
        self.project.dpcm[m_index] = m_dpcm

    def _handle_dpcm(self, line):
        pass

    def _handle_groove(self, line):
        pass

    def _handle_usegroove(self, line):
        pass

    def _handle_inst2a03(self, line):
        pass

    def _handle_instvrc6(self, line):
        pass

    def _handle_instvrc7(self, line):
        pass

    def _handle_instfds(self, line):
        pass

    def _handle_instn163(self, line):
        pass

    def _handle_insts5b(self, line):
        pass

    def _handle_keydpcm(self, line):
        pass

    def _handle_fdswave(self, line):
        pass

    def _handle_fdsmod(self, line):
        pass

    def _handle_fdsmacro(self, line):
        pass

    def _handle_n163wave(self, line):
        pass

    def _handle_track(self, line):
        pass

    def _handle_columns(self, line):
        pass

    def _handle_order(self, line):
        pass

    def _handle_pattern(self, line):
        pass

    def _handle_row(self, line):
        pass

    def _process_line(self, line):
        first_word = line.split()[0]
        func = self.dispatch_table.get(first_word, self._nop)
        func(line)

    def exec(self, input_file):
        with open(input_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line: 
                    continue
                if line.startswith("#"): 
                    continue
                self._process_line(line)
        pass

