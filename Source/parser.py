# parser.py

from singleton import singleton

@singleton
class Parser:
    def __init__(self, project):
        self.project = project

    def _parse_track(self, track):
        print("Parsing TRACK {} \'{}\'".format( track.index, track.name))
        # TODO
        pass

    def exec(self):
        ''' 
        Adds self.resequenced_rows to each track in preparation for the MIDI export.
        '''
        for track in self.project.tracks:
            self._parse_track(track)
        pass

