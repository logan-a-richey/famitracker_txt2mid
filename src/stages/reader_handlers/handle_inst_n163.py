
# stages/reader_handlers/handle_inst_vrc7.py

import re

from stages.reader_handlers.base_handler import BaseHandler
from containers.inst_n163 import InstN163

class HandleInstN163(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = re.compile(r'''
            ^\s*
            (?P<tag>\w+)\s+
            (?P<index>\d+)\s+
            (?P<vol>\-?\d+)\s+
            (?P<arp>\-?\d+)\s+
            (?P<pit>\-?\d+)\s+
            (?P<hpi>\-?\d+)\s+
            (?P<dut>\-?\d+)\s+
            (?P<w_size>\d+)\s+
            (?P<w_pos>\d+)\s+
            (?P<w_count>\d+)\s+
            \"(?P<name>.*)\"
            .*$''', re.VERBOSE
        )

    def handle(self, line: str) -> bool:
        if x := self.pattern.match(line):
            # base instrument info
            tag = x.group('tag')
            index = int(x.group('index'))
            name = x.group('name')

            # macro indexes
            vol, arp, pit, hpi, dut = map(
                int, 
                x.group('vol', 'arp', 'pit', 'hpi', 'dut')
            )
            
            # special info
            w_size, w_pos, w_count = map(int, x.group('w_size', 'w_pos', 'w_count'))
            
            # create instrument object
            inst_object = InstN163(
                index, name, 
                vol, arp, pit, hpi, dut,
                w_size, w_pos, w_count
            )
            

            # add it to project
            self.project.instruments[index] = inst_object
            return True

        else:
            return False


