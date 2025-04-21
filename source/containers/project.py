# project.py

from typing import Dict, List
from containers.track import Track
from utils.reader import Reader
from utils.parser import Parser

class Project:
    def __init__(self):
        self.reader = Reader(self)
        self.parser = Parser(self)

        self.song_information: Dict[str, str] = {}
        self.global_settings: Dict[str, int] = {}
        self.tracks: List[Track] = []
    
    def __str__(self):
        """ Printable representation """
        text = ""
        text += "--- Song Information ---\n"
        for key, val in self.song_information.items():
            text += "{} : {}\n".format("\'{}\'".format(key).ljust(12), "\'{}\'".format(val))
        text += "\n"
        text += "--- Global Settings ---\n"
        for key, val in self.global_settings.items():
            text += "{} : {}\n".format("\'{}\'".format(key).ljust(12), val)
        text += "\n"
        text += "--- Tracks ---\n"
        total_tokens = 0
        for track in self.tracks:
            num_tokens = len(track.tokens)
            total_tokens += num_tokens
            text += "Track {} | {} | Tokens = {}\n".format(
                str(track.index).rjust(2), 
                "\'{}\'".format(track.name).ljust(20), 
                str(num_tokens).rjust(7)
            )
        text += "Total Tokens = {}\n".format(total_tokens)
        #text += "\n"
        return text

    def __repr__(self):
        return self.__str__()

