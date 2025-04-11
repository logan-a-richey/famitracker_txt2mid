# dpcm.py

from printable import Printable

class DPCM(Printable):
    def __init__(self, m_index: int, m_size: int, m_name: str): 
        self.m_index = m_index
        self.m_size  = m_size
        self.m_name = m_name

        self.m_data = []
