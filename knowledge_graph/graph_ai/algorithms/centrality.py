from abc import ABC, abstractmethod

class CentralityAlgorithm(ABC):
    @abstractmethod
    def compute_degree_centrality(self, projection_name: str, **kwargs):
        pass
        
    @abstractmethod
    def compute_betweenness_centrality(self, projection_name: str, **kwargs):
        pass
        
    @abstractmethod
    def compute_pagerank(self, projection_name: str, **kwargs):
        pass
