import numpy as np
import itertools
from collections import Counter

from sklearn.cluster import DBSCAN

from clustering.Cluster import Cluster
from clustering.PSOAlgorithm import PSOAlgorithm
from si.pso.CoPSO import CoPSO
from si.pso.IncreaseIWPSO import IncreaseIWPSO
from si.pso.StochasticIWPSO import StochasticIWPSO
from si.pso.DCMPSO import DCMPSO
from utils.charts import get_visual_cluster
from utils.misc import get_k_closest_bs, get_statistics


class DCM:
    def __init__(self, clustering_method, pso_algorithm, hetnet, timestep, min_samples=None, epsilon=None):
        self.method = clustering_method
        self.pso_algorithm = pso_algorithm
        self.data = []
        self.optimization_output = {}
        self.ue_list = hetnet.ue_list
        self.bs_list = hetnet.list_bs
        self.clusters = []
        self.priority_ues_weight = hetnet.env.priority_ues_weight
        self.ordinary_ues_weight = hetnet.env.ordinary_ues_weight
        self.outage_threshold = hetnet.env.outage_threshold
        self.timestep = timestep
        self.min_samples = min_samples
        self.epsilon = epsilon
        self.db = None

        # Extract UE position to a numpy array
        for ue in self.ue_list:
            self.data.append([ue.point.x, ue.point.y])
        self.data = np.array(self.data)

    # TODO: Incluir parametros na configuração DEFAULT
    def compute_clusters(self, population_size=200, max_steps=150):
        # Compute clusters
        if self.min_samples is None and self.epsilon is None:
            self.__get_optimized_cluster(population_size, max_steps)
        else:
            self.__get_static_cluster()

        self.__get_target_clusters()
        self.__get_evaluation_per_cluster()
        self.__compute_bs_per_cluster()

    def __get_static_cluster(self):
        self.db = DBSCAN(min_samples=self.min_samples, eps=self.epsilon).fit(self.data)

    def __get_optimized_cluster(self, population_size, max_steps):
        # Start the DCMPSO Engine
        pso = DCMPSO(self.data, population_size, max_steps, self.method, [0.9, 0.6], [2.05, 2.05])
        pso.search()
        self.min_samples = pso.g_best.best_min_samples
        self.epsilon = pso.g_best.best_epsilon

        # Generate the optimized cluster
        self.db = DBSCAN(min_samples=self.min_samples, eps=self.epsilon).fit(self.data)

        # Visual representation
        # get_visual_cluster(self.db, self.data)

    def __get_target_clusters(self):
        labels = self.db.labels_

        counter = Counter(labels.tolist())
        grouped_labels = [[k, ]*v for k, v in counter.items()]
        label_ids = []
        for group in grouped_labels:
            if group[0] is not -1:
                label_ids.append(group[0])

        for label_id in label_ids:
            new_cluster = Cluster(label_id, self.priority_ues_weight, self.ordinary_ues_weight, self.outage_threshold)
            for idx, l_ in enumerate(labels.tolist()):
                if label_id == l_:
                    new_cluster.ue_list.append(self.ue_list[idx])
            self.clusters.append(new_cluster)

    def __get_evaluation_per_cluster(self):
        for cluster in self.clusters:
            cluster.evaluate()
        self.clusters = [cluster for cluster in self.clusters if cluster.target_cluster is True]

    def __compute_bs_per_cluster(self):
        # Compute the closest BSs per cluster
        for cluster in self.clusters:
            bs_set = set()
            for ue in cluster.ue_list:
                closest_bs = get_k_closest_bs(ue, self.bs_list)
                bs_set.add(closest_bs[0])
            cluster.bs_list = bs_set

        # Compute difference between the BS sets
        for a, b in itertools.combinations(self.clusters, 2):
            a.bs_list = a.bs_list.difference(b.bs_list)
            b.bs_list = b.bs_list.difference(a.bs_list)

        # Debug
        for cluster in self.clusters:
            cluster.bs_list = list(sorted(cluster.bs_list))

    def optimization_engine(self, population_size, max_steps=20):
        if self.pso_algorithm is PSOAlgorithm.DCMPSO:
            pso = DCMPSO(self.data, population_size, max_steps, self.method, [0.9, 0.6], [2.05, 2.05])
            pso.search()
            self.optimization_output = {'DCMPSO-{}'.format(population_size): pso.mean_evaluation_evolution,
                                        'DCMPSO-{}-gbest'.format(population_size): pso.gbest_evaluation_evolution}
        elif self.pso_algorithm is PSOAlgorithm.CoPSO:
            pso = CoPSO(self.data, population_size, max_steps, self.method, [2.05, 2.05])
            pso.search()
            self.optimization_output = {'CoPSO-{}'.format(population_size): pso.mean_evaluation_evolution,
                                        'CoPSO-{}-gbest'.format(population_size): pso.gbest_evaluation_evolution}
        elif self.pso_algorithm is PSOAlgorithm.IncreaseIWPSO:
            pso = IncreaseIWPSO(self.data, population_size, max_steps, self.method, [0.4, 0.9], [2.0, 2.0])
            pso.search()
            self.optimization_output = {'IIWPSO-{}'.format(population_size): pso.mean_evaluation_evolution,
                                        'IIWPSO-{}-gbest'.format(population_size): pso.gbest_evaluation_evolution}
        elif self.pso_algorithm is PSOAlgorithm.StochasticIWPSO:
            pso = StochasticIWPSO(self.data, population_size, max_steps, self.method, [0.5, 1.0], [2.05, 2.05])
            pso.search()
            self.optimization_output = {'SIWPSO-{}'.format(population_size): pso.mean_evaluation_evolution,
                                        'SIWPSO-{}-gbest'.format(population_size): pso.gbest_evaluation_evolution}

    def get_cluster_analysis(self, population_size, max_steps=30):
        pso = DCMPSO(self.data, population_size, max_steps, self.method, [0.9, 0.6], [2.05, 2.05])
        pso.search()
        n_clusters, mean_cluster_size, n_outliers = get_statistics(pso.g_best.best_epsilon, pso.g_best.best_min_samples, self.data)
        return [n_clusters, mean_cluster_size, n_outliers]
