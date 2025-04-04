# groove.py

from printable import Printable
from typing import List

class Groove(Printable):
    def __init__(
        self,
        m_index: int,
        m_sizeof: int,
        m_seq: List[int]
    ):
        self.m_index = m_index
        self.m_sizeof = m_sizeof
        self.m_seq = m_seq

