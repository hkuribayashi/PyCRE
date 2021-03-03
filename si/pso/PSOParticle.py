import random
from abc import ABC
import numpy as np

from sklearn.cluster import DBSCAN, OPTICS
from sklearn.metrics import davies_bouldin_score, silhouette_score

from config.network import Network


class PSOParticle(ABC):

    def __init__(self, clustering_method, data_size, cognitive_factor):
        self.epsilon = random.uniform(100, np.sqrt(Network.DEFAULT.simulation_area))
        self.best_epsilon = self.epsilon
        self.min_samples = random.randint(10, data_size - 1)
        self.best_min_samples = self.min_samples
        self.evaluation = 10.0
        self.data_size = data_size
        self.clustering_method = clustering_method
        self.c1 = cognitive_factor[0]
        self.c2 = cognitive_factor[1]

    def evaluate(self, data):
        # TODO: Add more clustering methods
        clustering_method = DBSCAN(eps=self.epsilon, min_samples=self.min_samples).fit(data)

        # Get the cluster's labels and total number of clusters
        labels = clustering_method.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

        # Check if there is more than 1 cluster
        if n_clusters_ > 1:
            # Get the fitness evaluation

            current_evaluation = davies_bouldin_score(data, labels)
            # current_evaluation += (-1) * n_clusters_
            # n_noise_ = list(labels).count(-1)
            # current_evaluation += n_noise_
            current_evaluation += (-1) * silhouette_score(data, labels)

            # Updates the evaluation variables
            if current_evaluation < self.evaluation:
                self.evaluation = current_evaluation
                self.best_epsilon = self.epsilon
                self.best_min_samples = self.min_samples

    def update_position(self, g_best, inertia_weight):
        phi1 = random.random()
        phi2 = random.random()

        # Update epsilon velocity
        velocity_epsilon = (self.best_epsilon - self.epsilon) * phi1 * self.c1 + \
                           (g_best.best_epsilon - self.epsilon) * phi2 * self.c2

        # Update epsilon position
        self.epsilon = self.epsilon + (inertia_weight * velocity_epsilon)

        # Epsilon Constraint
        if self.epsilon < 100:
            self.epsilon = 100

        # Update Min samples velocity
        velocity_min_samples = (self.best_min_samples - self.min_samples) * phi1 * self.c1 + \
                               (g_best.best_min_samples - self.min_samples) * phi2 * self.c2

        # Update Min samples position
        self.min_samples = int(self.min_samples + (inertia_weight * velocity_min_samples))

        # Min Samples Constraint
        if self.min_samples < 10:
            self.min_samples = 10
        elif self.min_samples > self.data_size:
            self.min_samples = self.data_size - 1


class PSOParticle2(ABC):

    def __init__(self, clustering_method, data_size, cognitive_factor):
        self.xi = random.uniform(0.000001, 0.999999)
        self.best_xi = self.xi
        self.min_samples = random.uniform(0.000001, 0.999999)
        self.best_min_samples = self.min_samples
        self.min_cluster_size = random.uniform(0.000001, 0.999999)
        self.best_min_cluster_size = self.min_cluster_size
        self.evaluation = 10.0
        self.data_size = data_size
        self.clustering_method = clustering_method
        self.c1 = cognitive_factor[0]
        self.c2 = cognitive_factor[1]

    def evaluate(self, data):
        # TODO: Add more clustering methods
        clustering_method = OPTICS(min_samples=self.min_samples, xi=self.xi, min_cluster_size=self.min_cluster_size).fit(data)

        # Get the cluster's labels and total number of clusters
        labels = clustering_method.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

        # Check if there is more than 1 cluster
        if n_clusters_ > 1:
            # Get the fitness evaluation
            current_evaluation = davies_bouldin_score(data, labels)

            # Updates the evaluation variables
            if current_evaluation < self.evaluation:
                self.evaluation = current_evaluation
                self.best_xi = self.xi
                self.best_min_cluster_size = self.min_cluster_size
                self.best_min_samples = self.min_samples

    def update_position(self, g_best, inertia_weight):
        phi1 = random.random()
        phi2 = random.random()

        # Update xi velocity
        velocity_xi = (self.best_xi - self.xi) * phi1 * self.c1 + \
                           (g_best.best_xi - self.xi) * phi2 * self.c2

        # Update xi position
        self.xi = self.xi + (inertia_weight * velocity_xi)

        # Xi's Constraint
        if self.xi <= 0:
            self.xi = 0.000001
        if self.xi >= 1:
            self.xi = 0.999999

        phi1 = random.random()
        phi2 = random.random()

        # Update Min samples velocity
        velocity_min_samples = (self.best_min_samples - self.min_samples) * phi1 * self.c1 + \
                               (g_best.best_min_samples - self.min_samples) * phi2 * self.c2

        # Update Min samples position
        self.min_samples = self.min_samples + (inertia_weight * velocity_min_samples)

        # Min Samples Constraint
        if self.min_samples <= 0:
            self.min_samples = 0.000001
        elif self.min_samples >= 1:
            self.min_samples = 0.999999

        phi1 = random.random()
        phi2 = random.random()

        # Update Min Cluster Size velocity
        velocity_min_cluster_size = (self.best_min_cluster_size - self.min_cluster_size) * phi1 * self.c1 + \
                               (g_best.best_min_cluster_size - self.min_cluster_size) * phi2 * self.c2

        # Update Min samples position
        self.min_cluster_size = self.min_cluster_size + (inertia_weight * velocity_min_cluster_size)

        # Min Samples Constraint
        if self.min_cluster_size <= 0:
            self.min_cluster_size = 0.000001
        elif self.min_cluster_size >= 1:
            self.min_cluster_size = 0.999999
