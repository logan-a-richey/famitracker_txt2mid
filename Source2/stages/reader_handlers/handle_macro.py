# stages/reader/handle_macro.py

import re

from stages.reader_handlers.base_handler import BaseHandler
from containers.macro import Macro

class HandleMacro(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        # ^\s*(\w+)\s+([0-4])\s+(\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\d+)\s*\:\s*(\d+(?:\s+\-?\d+)*)$
        self.pattern = re.compile(r'''
            ^\s*                # start of string (optional leading space)
            (\w+)\s+            # macro tag
            ([0-4])\s+          # macro type
            (\d+)\s+            # macro index
            (\-?\d+)\s+         # macro loop
            (\-?\d+)\s+         # macro release
            (\d+)\s*\:\s*       # macro setting
            (\d+(?:\s+\-?\d+)*) # macro sequence
            $                   # end of string
            ''', re.VERBOSE)

    def handle(self, line: str):
        if x := self.pattern.match(line):
            macro_tag = x.group(1)
            macro_type, macro_index, macro_loop, macro_release, macro_setting = list(map(int, x.group(2, 3, 4, 5, 6)))
            macro_sequence = list(map(int, re.findall(r'(\-?\d+)', x.group(7))))
            macro_object = Macro(
                macro_tag,
                macro_type,
                macro_index,
                macro_loop,
                macro_release,
                macro_setting, 
                macro_sequence
            )
            macro_key = "{}.{}.{}".format(macro_tag, macro_type, macro_index)
            self.project.macros[macro_key] = macro_object
        else:
            print("[WARN] Did not match! \'{}\'".format(line))
        return
