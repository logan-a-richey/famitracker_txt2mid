# stages/reader/handle_dpcm_def.py

from utils.regex_patterns import RegexPatterns
from stages.reader_handlers.base_handler import BaseHandler
from containers.dpcm import Dpcm

class HandleDpcmDef(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = RegexPatterns.patterns['dpcm_def']

    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match")
            return 1

        index, size = list(map(int, x.group('index', 'size')))
        name = x.group('name')
        dpcm_object = Dpcm(index, size, name)
        
        self.project.dpcm[index] = dpcm_object
        self.project.target_dpcm_index = index
        return 0

