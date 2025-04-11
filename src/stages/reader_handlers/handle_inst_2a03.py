# stages/reader_handlers/handle_inst_2a03.py

import re

from stages.reader_handlers.base_handler import BaseHandler
from containers.inst_2a03 import Inst2A03

class HandleInst2A03(BaseHandler):
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
            (?P<seq_dut>\-?\d+)\s+\"
            (?P<name>.*?)\".*$''', re.VERBOSE
        )

    def handle(self, line: str):
        if x := self.pattern.match(line):
            inst_tag = x.group('tag') 
            inst_index, seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut = \
                list(map(int, x.group(
                    'index', 'seq_vol', 'seq_arp', 
                    'seq_pit', 'seq_hpi', 'seq_dut'
                )
            ))
            inst_name = x.group('name')
            
            inst_object = Inst2A03(
                inst_index,
                inst_name,
                seq_vol,
                seq_arp,
                seq_pit,
                seq_hpi,
                seq_dut
            )
            self.project.instruments[inst_index] = inst_object
        
        else:
            print("[WARN] Could not handle line! {}".format(line))



