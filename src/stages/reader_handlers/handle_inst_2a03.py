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
            (?P<vol>\-?\d+)\s+
            (?P<arp>\-?\d+)\s+
            (?P<pit>\-?\d+)\s+
            (?P<hpi>\-?\d+)\s+
            (?P<dut>\-?\d+)\s+
            \"(?P<name>.*?)\"
            .*$''', re.VERBOSE
        )

    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match")
            return 1

        # basic info
        inst_tag = x.group('tag') 
        inst_index = int(x.group('index'))
        inst_name = x.group('name')
        
        # macros
        macro_types = ['vol', 'arp', 'pit', 'hpi', 'dut']
        macro_values = list(map(int, x.group(*macro_types)))

        # create instrument object
        inst_object = Inst2A03(inst_index, inst_name, *macro_values)

        # assign macros to instrument
        for i, macro_type in enumerate(macro_types):
            macro_value = getattr(inst_object, macro_type)
            key = "CHIP={}:TYPE={}:INDEX={}".format(inst_tag.replace("INST", "MACRO"), i, macro_value)
            macro_object = self.project.macros.get(key, None)
            if macro_object:
                inst_object.macros[macro_type] = macro_object

        # add it to project
        self.project.instruments[inst_index] = inst_object
        return 0



