# handle_track_columns.py

import re

from stages.reader_handlers.base_handler import BaseHandler

class HandleTrackColumns(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = re.compile(r'''
            ^\s*
            (?P<tag>COLUMNS)
            \s*\:\s*
            (?P<data>.*)
            $
            ''', re.VERBOSE
        )

    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match")
            return 1
        
        # parse regex
        eff_cols = list(map(
            int, 
            re.findall(r'\d+', x.group('data'))
        ))
        num_cols = len(eff_cols)
        
        # get target track
        target_track = self.project.tracks[self.project.target_track]

        # add data to target track:
        target_track.num_cols = num_cols
        target_track.eff_cols = eff_cols

        return 0

