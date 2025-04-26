from abc import ABC, abstractmethod

class ClusteringRepository(ABC):
    @abstractmethod
    def cluster(self, data, n):
        pass
