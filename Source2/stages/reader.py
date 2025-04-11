# stages/reader.py

from stages.reader_handlers.HandleSongInformation import HandleSongInformation

# TODO
class Reader:
    def __init__(self, project):
        self.project = project
        self.dispatch = {
            "TITLE":        HandleSongInformation(self.project),
            "AUTHOR":       HandleSongInformation(self.project),
            "COPYRIGHT":    HandleSongInformation(self.project),
            "COMMENT":      HandleSongInformation(self.project)
        }

        pass

    def _process_line(self, line: str) -> None:
        first_word = line.split()[0]
        handler = self.dispatch.get(first_word, None)
        if handler:
            print("Found!", line)
        

    def read(self, input_file: str) -> None:
        with open(input_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line[0] == "#":
                    continue
                self._process_line(line)

