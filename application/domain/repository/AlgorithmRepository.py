from abc import ABC, abstractmethod

class AlgorithmRepository(ABC):
    @abstractmethod
    def run(self):
        pass
