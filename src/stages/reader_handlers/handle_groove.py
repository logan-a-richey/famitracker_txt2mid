# stages/reader_handlers/handle_groove.py 

import re

from stages.reader_handlers.base_handler import BaseHandler
from containers.groove import Groove

class HandleGroove(BaseHandler):
    def __init__(self, project):
        super().__init__(project)

        self.pattern = re.compile(r'''
            ^\s*
            (?P<tag>\w+)
            \s+
            (?P<index>\d+)
            \s+
            (?P<sizeof>\d+)
            \s*\:\s*
            (?P<data>.*)
            $''', re.VERBOSE)

    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match")
            return 1

        index, sizeof = list(map(int, x.group('index', 'sizeof')))
        data = list(map(int, re.findall(r'\d+', x.group('data'))))
        groove_object = Groove(index, sizeof, data)
        self.project.grooves[index] = groove_object
        return 0
