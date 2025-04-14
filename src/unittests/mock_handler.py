# mock_handler.py

import re

class MockHandler:
    def __init__(self):
        self.pattern = re.compile(r'.*')

    def handle(self, line: str) -> int:
        x = self.pattern.match(line)
        if not x: 
            return 1
        return 0
