# stages/reader_handlers/HandleSongInformation.py

import re

from stages.reader_handlers.base_handler import BaseHandler

class HandleSongInformation(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = re.compile(r'''
            ^\s*                # optional leading space
            (?P<field>\w+)\s+\  # grab the first word
            "(?P<value>.*?)\"   # get text inside quotes (can include quotes)
            .*$''', re.VERBOSE
        )
    
    def handle(self, line: str):
        if x := self.pattern.match(line):
            # get key and value
            k = x.group('field')
            v = x.group('value')

            # update Project.song_information dictionary
            self.project.song_information[k] = v
        
        else:
            print("[WARN] Did not match! \'{}\'".format(line))


