# stages/reader_handlers/HandleSongInformation.py

class BaseHandler:
    def __init__(self, project):
        self.project = project

    def handle(self, line: str):
        print("Not implemented yet!")


class HandleSongInformation(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
    
    def handle(self, line: str):
        print("handled!")



