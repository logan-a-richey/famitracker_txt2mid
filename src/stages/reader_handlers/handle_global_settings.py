# stages/reader/handle_global_settings.py

import re

from stages.reader_handlers.base_handler import BaseHandler

class HandleGlobalSettings(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = re.compile(r'^\s*(?P<field>\w+)\s+(?P<value>\d+).*$')

    def handle(self, line: str) -> bool:
        if x := self.pattern.match(line):
            k = x.group('field') 
            v = int(x.group('value'))
            self.project.global_settings[k] = v
            return True
        else:
            print("[WARN] Regex failed. \'{}\'".format(line))
            return False
