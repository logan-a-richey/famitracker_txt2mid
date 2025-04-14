# stages/reader_handlers/handle_fds_wave.py 

import re
from stages.reader_handlers.base_handler import BaseHandler

class HandleFdsWave(BaseHandler):
    def __init__(self, project):
        super().__init__(project)

        # FDSWAVE [inst] : [data]
        self.pattern = re.compile(r'''
            ^\s*
            (?P<tag>\w+)
            \s+
            (?P<inst_index>\d+)
            \s*\:\s*
            (?P<data>.*)
            $''', re.VERBOSE
        )

    def handle(self, line: str) -> bool:
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match.")
            return 1

        inst_index = int(x.group('inst_index'))
        data = list(map(int, re.findall(r'\d+', x.group('data'))))

        inst_object = self.project.instruments.get(inst_index, None)
        if not inst_object:
            print("Instrument object key error.")
            return 1

        if not hasattr(inst_object, "fds_wave"):
            print("Instrument Attr error.")
            return 1

        inst_object.fds_wave = data
        return 0


