# stages/reader_handlers/handle_fds_mod.py 

import re
from utils.regex_patterns import RegexPatterns
from stages.reader_handlers.base_handler import BaseHandler

class HandleFdsMod(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = RegexPatterns.patterns['fds_mod']

    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match")
            return 1

        inst_index = int(x.group('inst_index'))
        data = list(map(int, re.findall(r'\d+', x.group('data'))))

        inst_object = self.project.instruments.get(inst_index, None)
        if not inst_object:
            print("[WARN] Could not add FDS_MOD. Instrument not of type InstFDS")
            return 1

        if not hasattr(inst_object, "fds_mod"):
            print("[WARN] Could not add FDS_Mod. Attribute error.")
            return 1

        inst_object.fds_mod = data
        return 0        

