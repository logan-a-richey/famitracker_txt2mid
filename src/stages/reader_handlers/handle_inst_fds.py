# stages/reader/handle_macro.py

import re

from stages.reader_handlers.base_handler import BaseHandler
from containers.inst_fds import InstFDS 

class HandleInstFDS(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = re.compile(r'''
            ^\s*
            (?P<tag>\w+)\s+
            (?P<index>\d+)\s+
            (?P<mod_enable>\d+)\s+
            (?P<mod_speed>\d+)\s+
            (?P<mod_depth>\d+)\s+
            (?P<mod_delay>\d+)\s+
            \"(?P<name>.*?)\"
            .*$''', re.VERBOSE
        )

    def handle(self, line: str) -> bool:
        if x := self.pattern.match(line):
            # base info
            inst_tag = x.group('tag')
            inst_index = x.group('index')
            inst_name = x.group('name')

            # special info
            fds_fields = ['mod_enable', 'mod_speed', 'mod_depth', 'mod_delay']
            fds_values = list(map(int, x.group(*fds_fields)))

            # create inst object
            inst_object = InstFDS(inst_index, inst_name, *fds_value)
           
            # add it to project
            self.project.instruments[inst_index] = inst_object
            return True

        else:
            return False

