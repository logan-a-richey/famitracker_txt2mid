# stages/reader/handle_global_settings.py

import re

from stages.reader_handlers.base_handler import BaseHandler

class HandleGlobalSettings(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = re.compile(r'^\s*(\w+)\s+(\d+).*$')

    def handle(self, line: str):
        if x := self.pattern.match(line):
            k = x.group(1) 
            v = int(x.group(2))
            self.project.global_settings[k] = v
        else:
            print("[WARN] Did not match! \'{}\'".format(line))
        return
