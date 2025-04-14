# stages/reader_handlers/handle_key_dpcm.py

from utils.regex_patterns import RegexPatterns

from stages.reader_handlers.base_handler import BaseHandler
from containers.key_dpcm import KeyDpcm
from containers.inst_2a03 import Inst2A03

class HandleKeyDpcm(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = RegexPatterns.patterns['key_dpcm']

    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match.")
            return 1

        # parse regex
        fields = ['inst', 'octave', 'note', 'sample', 'pitch', 'loop', 'loop_point', 'delta']
        values = list(map(int, x.group(*fields)))
        key_obj = KeyDpcm(*values)

        inst = self.project.instruments.get(values[0], None)
        if not inst:
            print("KeyError.")
            return 1

        if not isinstance(inst, Inst2A03):
            print("Not Inst2A03")
            return 1

        if not hasattr(inst, "key_dpcm"):
            print("AttributeError: does not have \'key_dpcm\'.")
            return 1

        # calculate integer famitracker note
        midi_int = values[1] * 12 + values[2]

        # add <class KeyDpcm> to 2A03 instrument map.
        inst.key_dpcm[midi_int] = key_obj
        return 0

