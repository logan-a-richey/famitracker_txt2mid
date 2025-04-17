# stages/reader_handlers/handle_track_order.py

import re
from utils.regex_patterns import RegexPatterns
from stages.reader_handlers.base_handler import BaseHandler

class HandleTrackOrder(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = RegexPatterns.patterns['order']

    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match")
            return 1
        
        # parse regex
        k = x.group('frame')
        v = re.findall(r'[0-9a-fA-F]{2}', x.group('list'))
    
        # get target track
        target_track = self.project.tracks[self.project.target_track]

        # add data
        target_track.orders[k] = v

        return 0

