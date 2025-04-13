# stages/reader_handlers/handle_use_groove.py 

import re

from stages.reader_handlers.base_handler import BaseHandler
from containers.groove import Groove

class HandleUseGroove(BaseHandler):
    def __init__(self, project):
        super().__init__(project)

        self.pattern = re.compile(r'''
            ^\s*
            (?P<tag>\w+)
            \s*\:\s*
            (?P<data>.*)
            $''', re.VERBOSE)

    def handle(self, line: str) -> bool:
        if x := self.pattern.match(line):
            data = list(map(int, re.findall(r'\d+', x.group('data'))))
            self.project.use_groove = data
            return True

        else:
            return False
