# parser.py

from singleton import singleton

@singleton
class Parser:
    def __init__(self, project):
        self.project = project

    def exec(self):
        pass

