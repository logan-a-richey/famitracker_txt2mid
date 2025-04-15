# parser.py

import re
from typing import List, Dict, Set, Tuple, Union
#from utils.singleton import SingletonMeta

from containers.track import Track

class Parser:
    regex_patterns = {
        # global effects
        "bxx" : re.compile(r'[B][0-9A-F]{2}'), # order skip to xx
        "cxx" : re.compile(r'[B][0-9A-F]{2}'), # order skip stop song
        "dxx" : re.compile(r'[B][0-9A-F]{2}'), # order skip next order at row xx
        "fxx" : re.compile(r'[F][0-9A-F]{2}'), # speed xx, if xx < SPLIT speed change, else tempo change
        "oxx" : re.compile(r'[O][0-9A-F]{2}'), # groove xx
        # column effects
        "qxx" : re.compile(r'[Q][0-9A-F]{2}'), # pitch bend up
        "rxx" : re.compile(r'[R][0-9A-F]{2}'), # pitch bend down
        "gxx" : re.compile(r'[G][0-9A-F]{2}'), # note delay start, xx fami ticks
        "sxx" : re.compile(r'[S][0-9A-F]{2}'), # note delay stop, xx fami ticks
        "0xx" : re.compile(r'[0][0-9A-F]{2}')  # arpeggio effect
    }

    def parse(self):
        ''' Prepare data for MIDI reading '''
        for track in self.project.tracks.values():
            self.parse_track(track)

