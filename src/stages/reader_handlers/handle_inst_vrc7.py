# stages/reader_handlers/handle_inst_vrc7.py

from utils.regex_patterns import RegexPatterns
from typing import List

from stages.reader_handlers.base_handler import BaseHandler
from containers.inst_vrc7 import InstVRC7

class HandleInstVRC7(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = RegexPatterns.patterns['inst_vrc7']

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
        patch = int(x.group('patch'))
        register_fields = ['r0','r1','r2','r3','r4','r5','r6','r7']
        register_values: List[int] = list(map(lambda x: int(x, 16), x.group(*register_fields)))

        # create instrument object
        inst_object = InstVRC7(index, name, patch, register_values)

        # add it to project
        self.project.instruments[index] = inst_object
        return 0
