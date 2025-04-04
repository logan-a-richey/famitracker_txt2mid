# project.py

from singleton import singleton
from reader import Reader
from parser import Parser
from exporter import Exporter

@singleton
class Project:
    def __init__(self):
        self.reader = Reader(self)
        self.parser = Parser(self)
        self.exporter = Exporter(self)

        # containers
        self.song_information = {}  # map<str, str>
        self.global_settings = {}   # map<str, int>
        self.macros = {}            # map<str, Macro>
        self.dpcm = {}              # map<str, DPCM>
        self.grooves = {}           # map<str, Groove>
        self.usegroove = []         # vec<int>
        self.instruments = {}       # map<str, BaseInstrument>
        self.tracks = []            # vec<Track>




