# handle_track_row.py

import re

from stages.reader_handlers.base_handler import BaseHandler

class HandleTrackRow(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        
        # #ROW [row] : [c0] : [c1] : [c2] ...
        self.pattern = re.compile(r'''
            \s*
            (?P<tag>\w+)
            \s+
            (?P<row>[0-9A-F]{2})
            \s*\:\s*
            (?P<list>
                (?:.{3}\s+.{2}\s+.{1}(?:\s+.{3})+)+
            ).*$''', re.VERBOSE)
        
        # ^\s+(?P<tag>\w+)\w+(?P<row>[0-9A-F]{2})\s*\:\s*(?P<list>.*)$

    def handle(self, line: str) -> int:
        # ROW 00 : D#4 00 F V00 : D#3 00 F V00 P7E : D#3 00 . ... : 0-# 01 . ... ...
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match.")
            return 1
        
        # get target track
        target_track = self.project.tracks[self.project.target_track]
        target_pattern = target_track._target_pattern

        row_int = int(x.group('row'), 16)
        tokens: List[str] = [token.strip() for token in line.split(":")[1:]]

        for col_int, token in enumerate(tokens):
            token_key = "PAT{}:ROW{}:COL{}".format(
                target_pattern,
                col_int,
                row_int
            )
            target_track.tokens[token_key] = token

        return 0



