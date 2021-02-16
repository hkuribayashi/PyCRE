import random
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import davies_bouldin_score

from config.network import Network


class Wolf:
    def __init__(self, data_size):
        self.epsilon = random.randint(1, np.sqrt(Network.DEFAULT.simulation_area))
        self.min_samples = random.randint(2, data_size - 1)
        self.evaluation = 10.0

    def evaluate(self, data):
        # TODO: Add more clustering methods
        clustering_method = DBSCAN(eps=self.epsilon, min_samples=self.min_samples).fit(data)

        # Get the cluster's labels and total number of clusters
        labels = clustering_method.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

        # Check if there is more than 1 cluster
        if n_clusters_ > 1:
            # Get the fitness evaluation
            self.evaluation = davies_bouldin_score(data, labels)

    def update_position(self, mean_min_samples, mean_episilon):
        pass