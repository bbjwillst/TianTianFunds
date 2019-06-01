import abc

class IDbHelper(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        pass
    @abc.abstractmethod
    def connectTo(self, db):
        pass
    @abc.abstractmethod
    def query(self):
        pass
    @abc.abstractmethod
    def save(self):
        pass
    @abc.abstractmethod
    def close(self):
        pass
