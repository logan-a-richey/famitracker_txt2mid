# stages/reader/handle_macro.py

import re

from stages.reader_handlers.base_handler import BaseHandler
from containers.macro import Macro

class HandleMacro(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = re.compile(r'''
            ^\s*                                # start of string
            (?P<tag>\w+)\s+                     # macro tag
            (?P<type>[0-4])\s+                  # macro type
            (?P<index>\d+)\s+                   # macro index
            (?P<loop>\-?\d+)\s+                 # macro loop
            (?P<release>\-?\d+)\s+              # macro release
            (?P<setting>\-?\d+)\s*\:\s*         # macro setting
            (?P<sequence>\-?\d+(?:\s+\-?\d+)*)  # macro sequence
            .*$                                 # end of string
            ''', re.VERBOSE
        )

    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match.")
            return 1

        # get macro tag (first word)
        macro_tag = x.group('tag')
        
        # give MACRO a full name [MACRO][TYPE] - this will make Instrument parsing easier.
        if macro_tag == "MACRO":
            macro_tag = "MACRO2A03"

        # get space separated integers
        macro_fields = ['type', 'index', 'loop', 'release', 'setting']
        macro_values = list(map(int, x.group(*macro_fields)))
        
        # get space separeted integer list after :
        macro_sequence = list(map(
            int, 
            re.findall(r'(\-?\d+)', x.group('sequence'))
        ))

        # create macro object
        macro_object = Macro(macro_tag, *macro_values, macro_sequence)

        # create macro key for lookup later
        # format: 'tag.type.index' (e.g. 'MACRO2A03.1.1')
        macro_key = "{}.{}.{}".format(macro_tag, macro_values[0], macro_values[1])

        # add it to project 
        self.project.macros[macro_key] = macro_object
        return 0


