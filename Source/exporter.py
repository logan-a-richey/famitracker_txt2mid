# exporter.py

from singleton import singleton

@singleton
class Exporter:
    def __init__(self, project):
        self.project = project

    def run(self):
        for line in track.data:
            print(line)

