# stages/reader_handlers/handle_track_pattern.py

from utils.regex_patterns import RegexPatterns
from stages.reader_handlers.base_handler import BaseHandler

class HandleTrackPattern(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = RegexPatterns.patterns['pattern']

    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match.")
            return 1

        # parse regex
        target_pattern = x.group('pattern')
        
        # get target track
        target_track = self.project.tracks[self.project.target_track]

        # add data
        target_track.patterns.append(target_pattern)
        target_track._target_pattern = target_pattern

        return 0
