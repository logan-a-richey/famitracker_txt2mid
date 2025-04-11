# containers/project.py

# TODO singleton
class Project:
    def __init__(self):
        self.song_information = {}
        self.global_settings = {}
        self.macros = {}

    def __str__(self):
        text = ""
        text += "--- Song Information ---\n{}\n\n".format(self.song_information)
        text += "--- Global Settings ---\n{}\n\n".format(self.global_settings)
        text += "--- Macros ---\n"
        for macro_key, macro_object in self.macros.items():
            text += "\'{}\' -> {}\n".format(macro_key, macro_object)
        text += "\n"

        return text

    def __repr__(self):
        return self.__str__()


