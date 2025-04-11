# stages/reader_handlers/handle_inst_2a03.py

import re
import sys

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

    def handle(self, line: str) -> bool:
        if x := self.pattern.match(line):
            # basic info
            inst_tag = x.group('tag') 
            inst_index = int(x.group('index'))
            inst_name = x.group('name')
            
            # macros
            vol, arp, pit, hpi, dut = map(int, x.group('vol', 'arp', 'pit', 'hpi', 'dut'))
            
            # create instrument object
            inst_object = Inst2A03(inst_index, inst_name, vol, arp, pit, hpi, dut)

            # load macros
            #print(" ".join(list(self.project.macros.keys())))
            #print(inst_tag)
            key0 = "{}.{}.{}".format(inst_tag.replace("INST","MACRO"), 0, vol)
            key1 = "{}.{}.{}".format(inst_tag.replace("INST","MACRO"), 1, arp)
            key2 = "{}.{}.{}".format(inst_tag.replace("INST","MACRO"), 2, pit)
            key3 = "{}.{}.{}".format(inst_tag.replace("INST","MACRO"), 3, hpi)
            key4 = "{}.{}.{}".format(inst_tag.replace("INST","MACRO"), 4, dut)
            
            macro_vol = self.project.macros.get(key0, None)
            macro_arp = self.project.macros.get(key1, None)
            macro_pit = self.project.macros.get(key2, None)
            macro_hpi = self.project.macros.get(key3, None)
            macro_dut = self.project.macros.get(key4, None)
           
            if macro_vol:
                inst_object.macros['vol'] = macro_vol
            if macro_arp:
                inst_object.macros['arp'] = macro_arp
            if macro_pit:
                inst_object.macros['pit'] = macro_pit
            if macro_hpi:
                inst_object.macros['hpi'] = macro_hpi
            if macro_dut:
                inst_object.macros['dut'] = macro_dut

            #if inst_object.macros:
            #    print("Macros were added! {}".format(inst_object.macros))

            # add it to project
            self.project.instruments[inst_index] = inst_object
            
            return True
        
        else:
            return False



