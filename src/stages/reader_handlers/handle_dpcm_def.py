# stages/reader/handle_dpcm_def.py

import re

from stages.reader_handlers.base_handler import BaseHandler
from containers.dpcm import Dpcm

class HandleDpcmDef(BaseHandler):
    def __init__(self, project):
        super().__init__(project)

        # DPCMDEF [index] [size] [name]
        self.pattern = re.compile(r'''
            ^\s*                # ignore leading whitespace
            (?P<tag>\w+)\s+     # grab the first word
            (?P<index>\d+)\s+   # grab the first number field
            (?P<size>\d+)\s*    # grab the second number field
            \"(?P<name>.*)\"    # grab the string between first and last quote
            .*$                 # ignore rest till end of the string
            ''', re.VERBOSE
        )

    def handle(self, line: str) -> bool:
        if x := self.pattern.match(line):
            fields = ['index', 'size']
            dpcm_object = Dpcm(list(map(int, x.group(*fields))), x.group('name'))
            
            self.project.dpcm[index] = dpcm_object
            self.project.target_dpcm_index = index

        else:
            return False

