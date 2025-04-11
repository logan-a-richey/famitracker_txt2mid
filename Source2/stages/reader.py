# stages/reader.py

from stages.reader_handlers.handle_song_information import HandleSongInformation
from stages.reader_handlers.handle_global_settings import HandleGlobalSettings
from stages.reader_handlers.handle_macro import HandleMacro

class Reader:
    def __init__(self, project):
        self.project = project

        self.dispatch = {}
        for tag in ["TITLE", "AUTHOR", "COPYRIGHT", "COMMENT"]:
            self.dispatch[tag] = HandleSongInformation(self.project)
        for tag in ["MACHINE", "FRAMERATE", "EXPANSION", "VIBRATO", "SPLIT", "N163CHANNELS"]:
            self.dispatch[tag] = HandleGlobalSettings(self.project)
        for tag in [ "MACRO", "MACROVRC6", "MACRON163", "MACROS5B"]:
            self.dispatch[tag] = HandleMacro(self.project)
# TODO            
#"DPCMDEF"
#"DPCM"
#"GROOVE"
#"USEGROOVE"
#"INST2A03"
#"INSTVRC6"
#"INSTVRC7"
#"INSTFDS"
#"INSTN163"
#"INSTS5B"
#"KEYDPCM"
#"FDSWAVE"
#"FDSMOD"
#"FDSMACRO"
#"N163WAVE"
#"TRACK"
#"COLUMNS"
#"ORDER"
#"PATTERN"
#"ROW"
        pass

    def _process_line(self, line: str) -> None:
        first_word = line.split()[0]
        handler = self.dispatch.get(first_word, None)
        if handler:
            #print("Found!", line)
            handler.handle(line) 

    def read(self, input_file: str) -> None:
        with open(input_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line[0] == "#":
                    continue
                self._process_line(line)

