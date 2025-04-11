# stages/reader.py

from stages.reader_handlers.handle_song_information import HandleSongInformation
from stages.reader_handlers.handle_global_settings import HandleGlobalSettings
from stages.reader_handlers.handle_macro import HandleMacro
from stages.reader_handlers.handle_inst_2a03 import HandleInst2A03
from stages.reader_handlers.handle_inst_vrc7 import HandleInstVRC7
from stages.reader_handlers.handle_inst_n163 import HandleInstN163
from stages.reader_handlers.handle_inst_fds import HandleInstFDS

# TODO            
#"DPCMDEF"
#"DPCM"

#"GROOVE"
#"USEGROOVE"

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

class Reader:
    def __init__(self, project):
        self.project = project

        self.dispatch = {}
        
        # init dispatch table
        for tag in ["TITLE", "AUTHOR", "COPYRIGHT", "COMMENT"]:
            self.dispatch[tag] = HandleSongInformation(self.project)
        
        for tag in ["MACHINE", "FRAMERATE", "EXPANSION", "VIBRATO", "SPLIT", "N163CHANNELS"]:
            self.dispatch[tag] = HandleGlobalSettings(self.project)
        
        for tag in [ "MACRO", "MACROVRC6", "MACRON163", "MACROS5B"]:
            self.dispatch[tag] = HandleMacro(self.project)

        for tag in ["INST2A03", "INSTVRC6", "INSTS5B"]:
            self.dispatch[tag] = HandleInst2A03(self.project)
        
        self.dispatch["INSTVRC7"] = HandleInstVRC7(self.project)
        self.dispatch["INSTFDS"] = HandleInstFDS(self.project)
        self.dispatch["INSTN163"] = HandleInstN163(self.project)

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

