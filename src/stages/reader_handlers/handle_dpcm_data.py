# stages/reader_handlers/handle_dpcm_data.py

import re
from utils.regex_patterns import RegexPatterns
from stages.reader_handlers.base_handler import BaseHandler

class HandleDpcmData(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = RegexPatterns.patterns['dpcm']

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

