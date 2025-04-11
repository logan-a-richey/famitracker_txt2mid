
# stages/reader_handlers/handle_inst_vrc7.py

import re

from stages.reader_handlers.base_handler import BaseHandler
from containers.instrument import InstN163

class HandleInstN163(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = re.compile(r'''
            ^\s*
            (?P<tag>\w+)\s+
            (?P<index>\d+)\s+
            (?P<seq_vol>\-?\d+)\s+
            (?P<seq_arp>\-?\d+)\s+
            (?P<seq_pit>\-?\d+)\s+
            (?P<seq_hpi>\-?\d+)\s+
            (?P<seq_dut>\-?\d+)\s+
            (?P<w_size>\d+)\s+
            (?P<w_pos>\d+)\s+
            (?P<w_count>\d+)\s+\"
            (?P<name>)\s+\".*$''', re.VERBOSE
        )

    def handle(self, line: str):

        if x := self.pattern.match(line):
            inst_object = InstN163(
                inst_index,
                inst_name
            )
            self.project.instruments[inst_index] = inst_object
        
        else:
            print("[WARN] Could not handle line! {}".format(line))
