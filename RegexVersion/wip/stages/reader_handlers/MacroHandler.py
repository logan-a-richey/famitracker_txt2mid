# MacroHandler.py

import re
from containers.macro import Macro

class MacroHandler(LineHandler):
    pattern = re.compile(
        r'^\s*(MACRO\w*)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s*:\s*((?:-?\d+\s*)+)$'
    )

    def handle(self, match, reader):
        macro_tag = match.group(1)
        macro_type, macro_index, macro_loop, macro_release, macro_setting = list(map(int, match.group(2, 3, 4, 5, 6)))
        macro_sequence = list(map(int, re.findall(r'-?\d+', match.group(7))))

        macro_key = "{}.{}.{}".format(macro_tag, macro_type, macro_index)
        macro_object = Macro(
            macro_tag, macro_type, macro_index, macro_loop,
            macro_release, macro_setting, macro_sequence
        )
        reader.project.macros[macro_key] = macro_object
        print(macro_object)
