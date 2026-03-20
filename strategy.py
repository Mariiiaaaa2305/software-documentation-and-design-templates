from abc import ABC, abstractmethod

class OutputStrategy(ABC):
    @abstractmethod
    def save(self, data):
        pass