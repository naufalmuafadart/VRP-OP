from application.domain.repository.ClusteringRepository import ClusteringRepository
from sklearn.cluster import KMeans
import numpy as np

class KMeansClusteringRepository(ClusteringRepository):
    def cluster(self, data, n):
        kmeans = KMeans(n_clusters=n, random_state=42)
        return kmeans.fit_predict(data)
