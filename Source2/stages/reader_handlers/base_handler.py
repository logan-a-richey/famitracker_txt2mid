# stages/reader_handlers/BaseHandler.py

class BaseHandler:
    def __init__(self, project):
        self.project = project

    def handle(self, line: str):
        print("Not implemented yet!")

