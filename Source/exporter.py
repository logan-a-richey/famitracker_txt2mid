# exporter.py

from singleton import singleton
#from lib_midi_writer_py.midi_writer import MidiWriter
from midi_writer import MidiWriter

@singleton
class Exporter:
    def __init__(self, project):
        self.project = project

    def _process_line(self, line):
        print(line)

    def run(self):
        for track in self.project.tracks:
            for line in track.data:
                self._process_line(line)

