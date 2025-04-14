# stages/reader_handlers/BaseHandler.py

from abc import ABC, abstractmethod
from utils.singleton import SingletonMeta

class BaseHandler(ABC, metaclass=SingletonMeta):
    '''Abstract base class'''

    def __init__(self, project):
        # link to project reference 
        self.project = project
        
    @abstractmethod
    def handle(self, line: str) -> int:
        ''' 
        Abstract method to be overridden by child class
        Contains logic to add data to `self.project`
        Return 0 for pass, return any other integer to signal an error has occured.
        '''
        return 1
