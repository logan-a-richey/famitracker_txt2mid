# containers/project.py

# TODO singleton
class Project:
    def __init__(self):
        self.song_information = {}
        self.global_settings = {}
        self.macros = {}

    def __str__(self):
        d = ""
        d += "--- Song Information ---\n{}\n".format(self.song_information)
        d += "--- Global Settings ---\n{}\n".format(self.global_settings)
        d += "--- Macros ---\n"
        for macro_key, macro_object in self.macros.items():
            d += "\'{}\' -> {}\n".format(macro_key, macro_object)
        
        return d

    def __repr__(self):
        return self.__str__()


