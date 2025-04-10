# LineHandler.py

class LineHandler:
    pattern = None  # Each subclass will set its own regex pattern

    def match(self, line: str):
        return self.pattern.match(line)

    def handle(self, match, reader):
        raise NotImplementedError
