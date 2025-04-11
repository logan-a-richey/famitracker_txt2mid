# printable.py

class Printable:
    '''contains __repr__ and __str__ methods to make a class debug-printable'''
    def __init__(self):
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__dict__}"
    
    def __str__(self):
        return self.__repr__()

