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

    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match")
            return 1
        
        # parse the data by converting space-separated hex_list to int_list
        data = list(map(
            lambda x: int(x, 16), 
            re.findall(r'[0-9a-fA-F]{2}', x.group('data'))
        ))
        
        # add it to existing dpcm object
        dpcm_object = self.project.dpcm.get(self.project.target_dpcm_index, None)
        if not dpcm_object:
            print("Dpcm KeyError.")
            return 1

        dpcm_object.data.extend(data)
        return 0

