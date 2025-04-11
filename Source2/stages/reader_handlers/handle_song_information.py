# stages/reader_handlers/HandleSongInformation.py

# from utils.singleton import Singleton
from stages.reader_handlers.base_handler import BaseHandler


class HandleSongInformation(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        #super(Singleton).__init__()
    
    def handle(self, line: str):
        print("handled!")

# TODO singleton test
#if __name__ == "__main__":
#    c = HandleSongInformation("")
#    d = HandleSongInformation("")
#    print(c is d)

