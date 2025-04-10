# project.py

import re
import json
from typing import List, Dict

class Project:
    def __init__(self):
        self.song_information: Dict[str, str] = {}
        self.global_settings: Dict[str, int] = {}
        self.macros: Dict[str, Macro] = {}
        self.instruments: Dict[str, Instrument] = {}
        self.tracks: List[Track] = []

    def __repr__(self) -> str:
        return "<class {}>".format(self.__class__.__name__)
