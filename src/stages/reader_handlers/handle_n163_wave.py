# stages/reader_handlers/handle_n163_wave.py 

import re
from stages.reader_handlers.base_handler import BaseHandler
from containers.inst_n163 import InstN163

class HandleN163Wave(BaseHandler):
    def __init__(self, project):
        super().__init__(project)

        # FDSWAVE [inst] : [data]
        self.pattern = re.compile(r'''
            ^\s*
            (?P<tag>\w+)
            \s+
            (?P<inst>\d+)
            \s+
            (?P<wave>\d+)
            \s*\:\s*
            (?P<data>.*)
            $
            ''', re.VERBOSE
        )

    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x:
            # did not get a regex match
            print("[WARN] Could not add N163Wave. Regex did not match")
            return 1
        
        inst_index = int(x.group('inst'))
        inst_object = self.project.instruments.get(inst_index, None)
        if not inst_object:
            print("[WARN] Could not add N163 Wave. Instrument KeyError.")
            return 1

        wave_index = int(x.group('wave'))
        wave_data = list(map(int, re.findall(r'\-?\d+', x.group('data'))))
        
        if not isinstance(inst_object, InstN163):
            print("[WARN] Could not add N163Wave. Instrument is not of type InstN163.")
            return 1

        if not hasattr(inst_object, "n163_waves"):
            print("[WARN] Could not add N163Wave. Instrument does not have attribute \'n163_waves\'")
            return 1

        inst_object.n163_waves[wave_index] = wave_data
        return 0 


