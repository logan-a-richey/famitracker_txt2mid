# utlis/printable.py

class Printable:
    def __repr__(self) -> str:
        return "<class {}, data {}>".format(self.__class__.__name__, self.__dict__)

    def __str__(self) -> str:
        return self.__repr__()

