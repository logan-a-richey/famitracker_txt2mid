#!/usr/bin/env python3

from abc import ABC, ABCMeta, abstractmethod

class Singleton:
    ''' Singleton base class to derive from '''
    _instances = {}
    # use __new__ method to preserve static variables
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(Singleton, cls).__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]

class SingletonMeta(ABCMeta):
    ''' Singleton metaclass implementation compatible with ABCMeta '''
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

###############################################################################

def test_derived_singleton() -> int:
    class MyClass(Singleton):
        static_var = "I'm a static/class variable"
        def __init__(self):
            self.value = 42
    
    # Derived Singleton Test
    a = MyClass()
    b = MyClass()

    print(a is b)                   # True — same instance
    print(MyClass.static_var)       # still accessible
    print(a.static_var)             # also accessible
    return 0

def test_metaclass_singleton() -> int:
    class MockHandler(ABC, metaclass=SingletonMeta):
        @abstractmethod
        def handle(self, data):
            pass

    class HandleType1(MockHandler):
        def handle(self, data):
            print("Handling Type I data:", data)


    class HandleType2(MockHandler):
        def handle(self, data):
            print("Handling Type II data:", data)
   
    # Singleton Metaclass Test
    a = HandleType1()
    b = HandleType1()
    c = HandleType2()
    d = HandleType2()

    a.handle("data 1")
    b.handle("data 2")
    c.handle("data 3")
    d.handle("data 4")

    print(a is b) # true
    print(c is d) # true
    print(a is d) # false - different handler types
    return 0

###############################################################################

def main() -> int:
    ''' Test different singleton behaviors '''
    funcs = [
        test_derived_singleton,
        test_metaclass_singleton
    ]
    for func in funcs:
        print("--- {} ---".format(func.__name__))
        func()
        print()

    return 0

if __name__ == "__main__":
    main()

  
