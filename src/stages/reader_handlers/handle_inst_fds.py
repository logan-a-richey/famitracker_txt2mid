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
            (?P<mod_delay>\d+)\s+\"
            (?P<name>.*?)\".*$''', re.VERBOSE
        )

    def handle(self, line: str):
        if x := self.pattern.match(line):
            inst_tag = x.group('tag')
            inst_index, mod_enable, mod_speed, mod_depth, mod_delay = \
                list(map(
                    int, 
                    x.group(
                        'index', 'mod_enable', 'mod_speed', 
                        'mod_depth', 'mod_delay'
                    )
                ))
            inst_name = x.group('name')

            inst_object = InstFDS(
                inst_index,
                inst_name,
                mod_enable,
                mod_speed,
                mod_depth,
                mod_delay
            )
            
            self.project.instruments[inst_index] = inst_object
        
        else:
            print("[WARN] Could not handle line! {}".format(line))

