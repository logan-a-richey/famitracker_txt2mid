# stages/reader.py

import sys

from stages.reader_handlers.handle_song_information import HandleSongInformation
from stages.reader_handlers.handle_global_settings import HandleGlobalSettings

from stages.reader_handlers.handle_macro import HandleMacro

from stages.reader_handlers.handle_inst_2a03 import HandleInst2A03
from stages.reader_handlers.handle_inst_vrc7 import HandleInstVRC7
from stages.reader_handlers.handle_inst_n163 import HandleInstN163
from stages.reader_handlers.handle_inst_fds import HandleInstFDS

from stages.reader_handlers.handle_dpcm_def import HandleDpcmDef
from stages.reader_handlers.handle_dpcm_data import HandleDpcmData

from stages.reader_handlers.handle_groove import HandleGroove
from stages.reader_handlers.handle_use_groove import HandleUseGroove

from stages.reader_handlers.handle_key_dpcm import HandleKeyDpcm

from stages.reader_handlers.handle_fds_wave import HandleFdsWave
from stages.reader_handlers.handle_fds_mod import HandleFdsMod
from stages.reader_handlers.handle_fds_macro import HandleFdsMacro
from stages.reader_handlers.handle_n163_wave import HandleN163Wave

# TODO
# from stages.reader_handlers.handle_track import HandleTrack
# from stages.reader_handlers.handle_track_columnss import HandleTrackColumns
# from stages.reader_handlers.handle_track_order import HandleTrackOrder
# from stages.reader_handlers.handle_track_pattern import HandleTrackPattern
# from stages.reader_handlers.handle_track_row import HandleTrackRow

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
            
            # groove info
            "GROOVE": HandleGroove(self.project),
            "USEGROOVE": HandleUseGroove(self.project),
            
            # instrument info
            **{tag: HandleInst2A03(self.project) for tag in [
                "INST2A03", "INSTVRC6", "INSTS5B"]},
            "INSTVRC7": HandleInstVRC7(self.project),
            "INSTFDS": HandleInstFDS(self.project),
            "INSTN163": HandleInstN163(self.project),

            # TODO special settings
            "KEYDPCM": HandleKeyDpcm(self.project),
            "FDSWAVE": HandleFdsWave(self.project),
            "FDSMOD": HandleFdsMod(self.project),
            "FDSMACRO": HandleFdsMacro(self.project),
            "N163WAVE": HandleN163Wave(self.project),
            
            # TODO track data:
            # "TRACK": HandleTrack(self.project),
            # "COLUMNS": HandleTrackColumns(self.project),
            # "ORDER": HandleTrackOrder(self.project);\,
            # "PATTERN": HandleTrackPattern(self.project),
            # "ROW": HandleTrackRow(self.project)
        }

    def _process_line(self, line: str) -> None:
        first_word = line.split()[0]

        if first_word == "BREAK":
            exit(0)

        handler = self.dispatch.get(first_word, None)
        if handler:
            res = handler.handle(line) 
            if res != 0:
                print("[ERROR] Error inside of {}. Scanning Line: \'{}\'".format(
                    handler.__name__,
                    line)
                )
                sys.exit(1)

    def read(self, input_file: str) -> None:
        with open(input_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line[0] == "#":
                    continue
                self._process_line(line)

