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

    def __repr__(self):
        dump = "<Class {}> Data:\n".format(self.__class__.__name__)

        dump += "\n** Song Information **\n"
        for k,v in self.song_information.items():
            dump += "{} -> {}\n".format(k,v)
            
        dump += "\n** Global Settings **\n"
        for k,v in self.global_settings.items():
            dump += "{} -> {}\n".format(k,v)

        dump += "\n** Macros **\n"
        for k,v in self.macros.items():
            dump += "{} -> {}\n".format(k,v)

        dump += "\n** DPCM **\n"
        for k,v in self.dpcm.items():
            dump += "{} -> {}\n".format(k,v)
        
        dump += "\n** Grooves **\n"
        for k,v in self.grooves.items():
            dump += "{} -> {}\n".format(k,v)

        dump += "\n** Use groove **\n"
        dump += "{}\n".format(self.usegroove)

        dump += "\n** Instruments **\n"
        for k,v in self.instruments.items():
            dump += "{} -> {}\n".format(k,v)

        dump += "\n** Tracks **\n"
        for k,v in enumerate(self.tracks):
            dump += "TRACK {}:\n{}\n".format(k,v)
        
        return dump

    def __str__(self):
        return self.__repr__()

