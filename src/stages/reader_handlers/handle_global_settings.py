# stages/reader_handlers/handle_global_settings.py

from utils.regex_patterns import RegexPatterns
from stages.reader_handlers.base_handler import BaseHandler

class HandleGlobalSettings(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = RegexPatterns.patterns['global_settings']
    
    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x:
            print("Regex does not match.")
            return 1

        k = x.group('field') 
        v = int(x.group('value'))
        self.project.global_settings[k] = v
        return 0 
        
