# reader.py

class Reader:
    def __init__(self, project):
        self.project = project

    def _process_line(self, line):
        pass

    def exec(self, input_file):
        with open(input_file, 'r') as file:
            for line in file:
                self._process_line(line)
        pass

