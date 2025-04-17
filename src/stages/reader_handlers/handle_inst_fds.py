# stages/reader_handlers/handle_macro.py

from utils.regex_patterns import RegexPatterns

from stages.reader_handlers.base_handler import BaseHandler
from containers.inst_fds import InstFDS 

class HandleInstFDS(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = RegexPatterns.patterns['inst_fds']

    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match")
            return 1

        # base info
        inst_tag = x.group('tag')
        inst_index = int(x.group('index'))
        inst_name = x.group('name')

        # special info
        fds_fields = ['mod_enable', 'mod_speed', 'mod_depth', 'mod_delay']
        fds_values = list(map(int, x.group(*fds_fields)))

        # create inst object
        inst_object = InstFDS(inst_index, inst_name, *fds_values)
       
        # add it to project
        self.project.instruments[inst_index] = inst_object
        return 0


