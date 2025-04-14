# handle_track.py

import re

from stages.reader_handlers.base_handler import BaseHandler
from containers.track import Track

class HandleTrack(BaseHandler):
    def __init__(self, project):
        super().__init__(project)

        # line = \"TRACK 120   3 160 "New song"\"
        self.pattern = re.compile(r'''
            ^\s*
            (?P<tag>\w+)
            \s+
            (?P<pattern>\d+)
            \s+
            (?P<speed>\d+)
            \s+
            (?P<tempo>\d+)
            \s*
            \"(?P<name>.*)\".*$
            ''', re.VERBOSE
        )

    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match.")
            return 1
        
        # parse regex
        num_rows, speed, tempo = list(map(int, x.group('pattern', 'speed', 'tempo')))
        name = x.group('name')

        # create track object
        track_object = Track(num_rows, speed, tempo, name)

        # get track index
        self.project.target_track = track_object.index
        
        # add it to project
        self.project.tracks[track_object.index] = track_object

        return 0
