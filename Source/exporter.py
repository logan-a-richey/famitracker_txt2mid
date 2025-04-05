# exporter.py

from singleton import singleton

@singleton
class Exporter:
    def __init__(self, project):
        self.project = project

    # TODO
    def exec(self):
        pass

