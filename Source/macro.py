# macro.py

from typing import List

class Macro:
    def __init__(
        self,
        m_chip: str,
        m_type: int, 
        m_index: int, 
        m_loop: int, 
        m_release: int, 
        m_setting: int, 
        m_seq: List[int],
    ):
        self.m_chip = m_chip
        self.m_type = m_type
        self.m_index = m_index
        self.m_loop = m_loop
        self.m_release = m_release
        self.m_setting = m_setting
        self.m_seq= m_seq
    
    def __repr__(self) -> str:
        #return "<class {}>".format(self.__class__.__name__)
        return f"{self.__class__.__name__}: {self.__dict__}"


