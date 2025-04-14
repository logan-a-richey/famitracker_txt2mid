# stages/reader_handlers/handle_fds_mod.py 

import re
from stages.reader_handlers.base_handler import BaseHandler

class HandleFdsMod(BaseHandler):
    def __init__(self, project):
        super().__init__(project)

        # FDSWAVE [inst] : [data]
        self.pattern = re.compile(r'''
            ^\s*
            (?P<tag>\w+)
            \s+
            (?P<inst_index>\d+)
            \s*\:\s*
            (?P<data>.*)
            $''', re.VERBOSE
        )

    def handle(self, line: str) -> bool:
        if x := self.pattern.match(line):
            inst_index = int(x.group('inst_index'))
            data = list(map(int, re.findall(r'\d+', x.group('data'))))

            inst_object = self.project.instruments.get(inst_index, None)
            if inst_object:
                if hasattr(inst_object, "fds_mod"):
                    inst_object.fds_mod = data
                    return True
                else:
                    print("[WARN] Could not add FDS_MOD. Attribute error: \'fds_mod\'")
                    return False
            else:
                print("[WARN] Could not add FDS_MOD. Instrument index KeyError.")
        
        else:
            return False
                


