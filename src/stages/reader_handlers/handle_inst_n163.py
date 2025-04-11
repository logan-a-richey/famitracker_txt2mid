
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
            inst_tag = x.group('tag')
            inst_index = int(x.group('index'))
            inst_name = x.group('name')

            # macros
            macro_types = ['vol', 'arp', 'pit', 'hpi', 'dut']
            macro_values = list(map(int, x.group(*macro_types)))

            # special info
            namco_fields = ['w_size', 'w_pos', 'w_count']
            namco_values = list(map(int, x.group(*namco_fields)))
            
            # create instrument object
            inst_object = InstN163(inst_index, inst_name, *macro_values, *namco_values)

            # assign macros to instrument
            for i, macro_type in enumerate(macro_types):
                macro_value = getattr(inst_object, macro_type)
                key = "{}.{}.{}".format(inst_tag.replace("INST", "MACRO"), i, macro_value)
                if (macro_object := self.project.macros.get(key, None)):
                    inst_object.macros[macro_type] = macro_object

            # add it to project
            self.project.instruments[inst_index] = inst_object
            return True

        else:
            return False


