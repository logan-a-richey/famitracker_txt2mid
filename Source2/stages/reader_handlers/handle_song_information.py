# stages/reader_handlers/HandleSongInformation.py

import re

from stages.reader_handlers.base_handler import BaseHandler

class HandleSongInformation(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = re.compile(r'^\s*(\w+)\s+\"(.*?)\"$')
    
    def handle(self, line: str):
        # TITLE "asdf"
        if x := self.pattern.match(line):
            k = x.group(1)
            v = x.group(2)
            self.project.song_information[k] = v
        else:
            print("[WARN] Did not match! \'{}\'".format(line))
        return

# TODO singleton test
#if __name__ == "__main__":
#    c = HandleSongInformation("")
#    d = HandleSongInformation("")
#    print(c is d)

