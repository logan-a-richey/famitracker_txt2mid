# stages/reader_handlers/handle_use_groove.py 

import re
from utils.regex_patterns import RegexPatterns
from stages.reader_handlers.base_handler import BaseHandler
from containers.groove import Groove

class HandleUseGroove(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = RegexPatterns.patterns['use_groove']

    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match.")
            return 1

        data = list(map(int, re.findall(r'\d+', x.group('data'))))
        self.project.use_groove = data
        return 0

