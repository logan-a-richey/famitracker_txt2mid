# reader.py

import re

class Reader:
    def __init__(self, project):
        self.project = project
        self.dispatch_table = {
            "TITLE": self._handle_title,
            "AUTHOR": self._handle_author,
            "COPYRIGHT": self._handle_copyright,
            "COMMENT": self._handle_comment,
            "MACHINE": self._handle_machine,
            "FRAMERATE": self._handle_framerate,
            "EXPANSION": self._handle_expansion,
            "VIBRATO": self._handle_vibrato,
            "SPLIT": self._handle_split,
            "N163CHANNELS": self._handle_n163channels,
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

    def _nop(self, line):
        pass

    def _handle_title(self, line):
        pass

    def _handle_author(self, line):
        pass

    def _handle_copyright(self, line):
        pass

    def _handle_comment(self, line):
        pass

    def _handle_machine(self, line):
        pass

    def _handle_framerate(self, line):
        pass

    def _handle_expansion(self, line):
        pass

    def _handle_vibrato(self, line):
        pass

    def _handle_split(self, line):
        pass

    def _handle_n163channels(self, line):
        pass

    def _handle_macro(self, line):
        pass

    def _handle_macrovrc6(self, line):
        pass

    def _handle_macron163(self, line):
        pass

    def _handle_macros5b(self, line):
        pass

    def _handle_dpcmdef(self, line):
        pass

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

