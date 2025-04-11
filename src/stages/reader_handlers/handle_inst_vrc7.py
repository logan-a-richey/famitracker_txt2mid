# stages/reader_handlers/handle_inst_vrc7.py

import re

from stages.reader_handlers.base_handler import BaseHandler
from containers.inst_vrc7 import InstVRC7

class HandleInstVRC7(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = re.compile(r'''
            ^\s*
            (?P<tag>\w+)\s+
            (?P<index>\d+)\s+
            (?P<patch>\d+)\s+
            (?P<r0>[0-9a-fA-F]{2})\s+
            (?P<r1>[0-9a-fA-F]{2})\s+
            (?P<r2>[0-9a-fA-F]{2})\s+
            (?P<r3>[0-9a-fA-F]{2})\s+
            (?P<r4>[0-9a-fA-F]{2})\s+
            (?P<r5>[0-9a-fA-F]{2})\s+
            (?P<r6>[0-9a-fA-F]{2})\s+
            (?P<r7>[0-9a-fA-F]{2})\s+\"
            (?P<name>.*?)\".*$''', re.VERBOSE
        )

    def handle(self, line: str) -> bool:
        if x := self.pattern.match(line):
            # base instrument info
            tag = x.group('tag')
            inst_index = x.group('index')
            inst_name = x.group('name')

            # special info
            patch = int(x.group('patch'))
            registers = list(map(
                lambda x: int(x, 16), 
                x.group('r0','r1','r2','r3','r4','r5','r6','r7')
            ))

            # create instrument object
            inst_object = InstVRC7(
                index, inst_name, 
                patch, registers
            )

            # add it to project
            self.project.instruments[index] = inst_object
            return True

        else:
            print("[WARN] Regex failed. \'{}\'".format(line))
            return False

