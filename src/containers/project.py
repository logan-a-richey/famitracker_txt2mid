# containers/project.py

from typing import List, Dict

from containers.macro import Macro
from containers.base_inst import BaseInst
from containers.dpcm import Dpcm
from containers.groove import Groove
from containers.track import Track

# TODO singleton
class Project:
    def __init__(self):
        self.song_information: Dict[str, str] = {}
        self.global_settings: Dict[str, int] = {}
        self.macros: Dict[str, Macro] = {}
        self.instruments: Dict[int, BaseInst] = {}
        
        self.dpcm: Dict[int, Dpcm] = {}
        self.target_dpcm_index: int = 0 

        self.grooves: Dict[int, Groove] = {}
        self.usegroove: List[int] = []

        self.tracks: Dict[int, Track] = {}
        self.target_track = 0

    def __str__(self):
        text = ""
        
        text += "--- Song Information ---\n"
        for k, v in self.song_information.items():
            text += "\'{}\': \'{}\'\n".format(k, v)
        text += "\n"

        text += "--- Global Settings ---\n"
        for k, v in self.global_settings.items():
            text += "\'{}\': {}\n".format(k, v)
        text += "\n"
        
        text += "--- Macros ---\n"
        for k, v in self.macros.items():
            text += "\'{}\': {}\n".format(k, v.macro_sequence)
        text += "\n"
        
        text += "--- Instruments ---\n"
        for k, v in self.instruments.items():
            text += "{}: <class {}> \'{}\'\n".format(k, type(v).__name__, v.name)
        text += "\n"
        
        text += "--- DPCM ---\n"
        for k, v in self.dpcm.items():
            text += "{}: <class {}>\n".format(k, type(v).__name__)
        text += "\n"

        text += "--- Grooves ---\n"
        for k, v in self.grooves.items():
            text += "{}: <class {}>\n".format(k, type(v).__name__)
        text += "\n"

        text += "--- Use Groove (List of Track indexes) ---\n"
        text += "{}\n".format(self.usegroove)
        text += "\n"

        text += "--- Tracks ---\n"
        for k, v in self.tracks.items():
            #text += "{}: <class {}> {}".format(k, type(v).__name__, v.name)
            text += "{}\n".format(v)
        
        return text

    def __repr__(self):
        return self.__str__()


