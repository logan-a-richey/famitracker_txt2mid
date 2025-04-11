# echo_buffer.py

class EchoBuffer:
    def __init__(self):
        self.data = []
        self.max_size = 4

    def peek(self, index):
        if len(self.data) == 0:
            return None

        if index == -1:
            return self.data[-1]

        return self.data[ min(len(self.data)-1, index) ]

    def push(self, item):
        self.data.insert(0, item)
        while len(self.data) > self.max_size:
            self.data.pop()

    def clear(self, item):
        self.data.clear()


