# dpcm.py

class DPCM:
    def __init__(
        self,
        m_index: int, 
        m_size: int, 
        m_name: str
    ): 
        self.m_index = m_index
        self.m_size  = m_size
        self.m_name = m_name

        self.m_data = []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__dict__}"
