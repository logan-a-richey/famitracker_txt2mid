# containers/project.py

# TODO singleton
class Project:
    def __init__(self):
        self.song_information = {}
        self.global_settings = {}

    def __str__(self):
        d = ""
        d += "--- Song Information ---\n{}\n".format(self.song_information)
        d += "--- Global Settings ---\n{}\n".format(self.global_settings)
        return d

    def __repr__(self):
        return self.__str__()


