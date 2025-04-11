
# stages/reader_handlers/handle_inst_vrc7.py

import re

from stages.reader_handlers.base_handler import BaseHandler
from containers.instrument import InstN163

class HandleInstN163(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        # TODO ? bad regex?
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
            (?P<w_count>\d+)\s+\"
            (?P<name>)\s+\".*$''', re.VERBOSE
        )

    def handle(self, line: str):
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
            
            # speical info
            w_size, w_pos, w_count = map(
                int, 
                x.group('w_size', 'w_pos', 'w_count')
            )
            
            # create instrument object
            inst_object = InstN163(
                index, name, 
                vol, arp, pit, hpi, dut,
                w_size, w_pos, w_count
            )
            
            # add macros # TODO
            # inst_object.macros[] = 

            # add it to project
            self.project.instruments[index] = inst_object
        
        else:
            print("[WARN] Could not handle line! {}".format(line))


