# echo_buffer.py

from typing import List, Union

class EchoBuffer:
    def __init__(self, max_size=4):
        self.lst: List[int] = []
        self.max_size: int = max_size

    def peek(self, index: int) -> Union[int, None]:
        # handle lower bound: no echo to return
        if len(self.lst) == 0:
            return None
        
        # handle upper bound (return last echo)
        if index > len(self.lst):
            return self.lst[-1]
        
        # return echo at position
        return self.lst[index]
    

    def push(self, item: int) -> None:
        # add a new echo
        self.lst.insert(0, item)

        # if size of stack is greater than max size, pop items until it is max size
        while len(self.lst) > self.max_size:
            self.lst.pop()

    def clear():
        # reset stack
        self.lst.clear()

    def __repr__(self) -> str:
        return "<class {}> data: {}".format(self.__class__.__name__, self.lst)

    def __str__(self) -> str:
        return self.__repr__()



