# stages/reader_handlers/handle_key_dpcm.py

import re

from stages.reader_handlers.base_handler import BaseHandler
from containers.key_dpcm import KeyDpcm
from containers.inst_2a03 import Inst2A03

class HandleKeyDpcm(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = re.compile(r'''
        ^\s*
        (?P<tag>\w+)
        \s+
        (?P<inst>\d+)
        \s+
        (?P<octave>\d+)
        \s+
        (?P<note>\d+)
        \s+
        (?P<sample>\d+)
        \s+
        (?P<pitch>\d+)
        \s+
        (?P<loop>\d+)
        \s+
        (?P<loop_point>\d+)
        \s+
        (?P<delta>\-?\d+)
        .*$
        ''', re.VERBOSE)

    def handle(self, line: str) -> bool:
        if x := self.pattern.match(line):
            #k = x.group('field') 
            #v = int(x.group('value'))
            #self.project.global_settings[k] = v
            fields = ['inst', 'octave', 'note', 'sample', 'pitch', 'loop', 'loop_point', 'delta']
            values = list(map(int, x.group(*fields)))
            key_obj = KeyDpcm(*values)

            inst = self.project.instruments.get(values[0], None)
            if inst:
                if hasattr(inst, "key_dpcm"):
                    midi_int = values[1] * 12 + values[2]
                    inst.key_dpcm[midi_int] = key_obj
                    return True
                else:
                    print("[WARN] Tried to add KeyDpcm to a non-2A03 instrument")
                    return False
            else:
                print("[WARN] Tried to add KeyDpcm to Instrument not in Project.instruments / KeyError.")
                return False
            return True
        
        else:
            return False


