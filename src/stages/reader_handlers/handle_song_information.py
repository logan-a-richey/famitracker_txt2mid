# stages/reader_handlers/HandleSongInformation.py

from utils.regex_patterns import RegexPatterns
from stages.reader_handlers.base_handler import BaseHandler

class HandleSongInformation(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = RegexPatterns.patterns['song_information']
    
    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match.")
            return 1

        # get key and value
        k = x.group('field')
        v = x.group('value')

        # update Project.song_information dictionary
        self.project.song_information[k] = v
        return 0
