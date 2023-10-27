from abc import ABC, abstractmethod

class UnitOfWork(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

class Repository(ABC):
    @abstractmethod
    def insert(self, query, value):
        pass

    @abstractmethod
    def update(self, query, value):
        pass

    @abstractmethod
    def delete(self, query, value):
        pass

    @abstractmethod
    def get(self, query, value):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

