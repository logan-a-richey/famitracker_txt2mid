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
            (?P<r7>[0-9a-fA-F]{2})\s+
            \"(?P<name>.*?)\"
            .*$''', re.VERBOSE
        )

    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match.")
            return 1

        # basic info
        tag = x.group('tag')
        index = x.group('index')
        name = x.group('name')

        # special info
        register_fields = ['r0','r1','r2','r3','r4','r5','r6','r7']
        register_values = list(map(lambda x: int(x, 16), x.group(*register)))

        # create instrument object
        inst_object = InstVRC7(index, name, patch, *register_values)

        # add it to project
        self.project.instruments[index] = inst_object
        return 0
