# project.py

from reader import Reader
from parser import Parser
from exporter import Exporter

class Project:
    def __init__(self):
        self.reader = Reader(self)
        self.parser = Parser(self)
        self.exporter = Exporter(self)

        # containers
        self.song_information = {}
        self.global_settings = {}
        self.macros = {}
        
        self.dpcm = {}
        self.grooves = {}
        self.usegroove = []
        
        self.instruments = {}
        self.tracks = []




