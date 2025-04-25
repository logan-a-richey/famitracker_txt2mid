# echo_buffer.py

class EchoBuffer:
    ''' Famitracker stack-like buffer for echo notes '''
    __slots__ = ('size', 'lst')

    def __init__(self):
        self.size = 4
        self.lst = []

    def peek(self, index: int):
        if len(self.lst) == 0:
            return None
        
        try:
            return self.lst[index]
        except IndexError:
            return self.lst[-1]

    def push(self, item: str):
        self.lst.insert(0, item)
        if len(self.lst) > self.size:
            self.lst.pop()

    def __str__(self):
        return "{}".format(self.lst)
