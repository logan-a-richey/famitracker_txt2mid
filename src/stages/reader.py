# stages/reader.py

from stages.reader_handlers.handle_song_information import HandleSongInformation
from stages.reader_handlers.handle_global_settings import HandleGlobalSettings

from stages.reader_handlers.handle_macro import HandleMacro

from stages.reader_handlers.handle_inst_2a03 import HandleInst2A03
from stages.reader_handlers.handle_inst_vrc7 import HandleInstVRC7
from stages.reader_handlers.handle_inst_n163 import HandleInstN163
from stages.reader_handlers.handle_inst_fds import HandleInstFDS

from stages.reader_handlers.handle_dpcm_def import HandleDpcmDef
from stages.reader_handlers.handle_dpcm_data import HandleDpcmData

class Reader:
    def __init__(self, project):
        self.project = project

        self.dispatch = {
            # project info
            **{tag: HandleSongInformation(self.project) for tag in [
                "TITLE", "AUTHOR", "COPYRIGHT", "COMMENT"]},
            **{tag: HandleGlobalSettings(self.project) for tag in [
                "MACHINE", "FRAMERATE", "EXPANSION", "VIBRATO", "SPLIT", "N163CHANNELS"]},
            
            # macro info
            **{tag: HandleMacro(self.project) for tag in [
                "MACRO", "MACROVRC6", "MACRON163", "MACROS5B"]},
            
            # dpcm info
            "DPCMDEF": HandleDpcmDef(self.project),
            "DPCM": HandleDpcmData(self.project),
            
            # TODO groove
            # TODO usegroove
            
            # instrument info
            **{tag: HandleInst2A03(self.project) for tag in [
                "INST2A03", "INSTVRC6", "INSTS5B"]},
            "INSTVRC7": HandleInstVRC7(self.project),
            "INSTFDS": HandleInstFDS(self.project),
            "INSTN163": HandleInstN163(self.project),

            # TODO special settings
            # "KEYDPCM": 
            # "FDSWAVE":
            # "FDSMOD":
            # "FDSMACRO":
            # "N163WAVE"
            
            # TODO track data:
            # "TRACK":
            # "COLUMNS":
            # "ORDER":
            # "PATTERN":
            # "ROW":
        }

    def _process_line(self, line: str) -> None:
        first_word = line.split()[0]

        if first_word == "BREAK":
            exit(0)

        handler = self.dispatch.get(first_word, None)
        if handler:
            res = handler.handle(line) 
            if not res:
                print("[WARN] Regex failed. Line: \'{}\'".format(line))

    def read(self, input_file: str) -> None:
        with open(input_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line[0] == "#":
                    continue
                self._process_line(line)

