import random

from sklearn.cluster import DBSCAN
from sklearn.metrics import davies_bouldin_score


class Particle:

    def __init__(self, clustering_method, data_size):
        self.epsilon = random.randint(1, 1000)
        self.best_epsilon = self.epsilon
        self.min_samples = random.randint(2, data_size - 1)
        self.best_min_samples = self.min_samples
        self.evaluation = 10.0
        self.data_size = data_size
        self.clustering_method = clustering_method

    def evaluate(self, data):
        # TODO: Add more clustering methods
        clustering_method = DBSCAN(eps=self.epsilon, min_samples=self.min_samples).fit(data)

        # Get the cluster's labels and total number of clusters
        labels = clustering_method.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

        # Check if there is more than 1 cluster
        if n_clusters_ > 1:
            try:
                current_evaluation = davies_bouldin_score(data, labels)
            except:
                print("n_clusters_: {}".format(n_clusters_))

            # Updates the evaluation variables
            if current_evaluation < self.evaluation:
                self.evaluation = current_evaluation
                self.best_epsilon = self.epsilon
                self.best_min_samples = self.min_samples

    def update_position(self, g_best, inertia_weight):
        phi1 = random.random()
        phi2 = random.random()

        # Update epsilon velocity
        velocity_epsilon = (self.best_epsilon - self.epsilon) * phi1 * 2.05 + \
                           (g_best.best_epsilon - self.epsilon) * phi2 * 2.05

        # Update epsilon position
        self.epsilon = self.epsilon + (inertia_weight * velocity_epsilon)

        # Epsilon Constraint
        if self.epsilon < 0:
            self.epsilon = 0.1

        # Update Min samples velocity
        velocity_min_samples = (self.best_min_samples - self.min_samples) * phi1 + \
                               (g_best.best_min_samples - self.min_samples) * phi2

        # Update Min samples position
        self.min_samples = int(self.min_samples + velocity_min_samples)

        # Min Samples Constraint
        if self.min_samples < 2:
            self.min_samples = 2
        elif self.min_samples > self.data_size:
            self.min_samples = self.data_size - 1