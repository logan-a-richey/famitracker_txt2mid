# stages/reader_handlers/handle_dpcm_data.py

import re
from stages.reader_handlers.base_handler import BaseHandler

class HandleDpcmData(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        
        # DPCM : [data]
        self.pattern = re.compile(r'''
            ^\s*            # optional leading whitespace
            (?P<tag>\w+)    # grab the first word
            \s*\:\s*        # div
            (?P<data>.*)    # grab the data
            $               # end of string
            ''', re.VERBOSE)

    def handle(self, line: str) -> bool:
        if x := self.pattern.match(line):
            data = list(map(lambda x: int(x, 16), re.findall(r'[0-9a-fA-F]{2}', x.group('data')))
            self.project.dpcm[self.project.target_dpcm_index].data.extend(data)

        else:
            return False
