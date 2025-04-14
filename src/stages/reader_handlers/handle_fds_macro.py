# stages/reader_handlers/handle_fds_macro.py

import re

from stages.reader_handlers.base_handler import BaseHandler
from containers.macro import Macro
from containers.inst_fds import InstFDS

class HandleFdsMacro(BaseHandler):
    def __init__(self, project):
        super().__init__(project)

        self.pattern = re.compile(r'''
            ^\s*
            (?P<tag>\w+)       # tag
            \s+
            (?P<inst>\d+)       # inst
            \s+
            (?P<type>\d+)       # type
            \s+
            (?P<loop>\-?\d+)    # loop
            \s+
            (?P<release>\-?\d+)    # release
            \s+
            (?P<setting>\d+)       # setting
            \s*\:\s*
            (?P<data>.*)$       # data
        ''', re.VERBOSE)

    def handle(self, line: str) -> bool:
        if x := self.pattern.match(line):
            # parse regex data
            macro_tag = x.group('tag')
            regex_fields = ['inst', 'type', 'loop', 'release', 'setting']
            inst_index, macro_type, macro_loop, macro_release, macro_setting = \
                list(map(int, x.group(*regex_fields)))

            macro_sequence = list(map(int, re.findall(r'\-?\d+', x.group('data'))))
            
            instrument_object = self.project.instruments.get(inst_index, None)
            
            if not instrument_object:
                print("[WARN] Could not add FDS_MACRO. Instrument KeyError.")
                return False
            
            if not isinstance(instrument_object, InstFDS):
                print("[WARN] Could not add FDS_MACRO. Instrument {} is not of type InstFDS.".format(inst_index))
                return False

            macro_object = Macro(
                macro_tag,
                macro_type, 
                0, # index (doesn't matter at this stage. This was mainly used for macro lookup.)
                macro_loop, 
                macro_release,
                macro_setting,
                macro_sequence
            )
            
            macro_types = ['vol', 'arp', 'pit', 'hpi', 'dut']
            instrument_object.macros[macro_types[macro_type]] = macro_object
            return True

        else:
            return False


