# singleton.py

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    pass

if __name__ == "__main__":
    class Dummy(Singleton):
        def __init__(self, value):
            self.value = value
    
    c = Dummy(3)
    d = Dummy(4)

    print(c is d) # true?
    print(c.value, d.value)


                
