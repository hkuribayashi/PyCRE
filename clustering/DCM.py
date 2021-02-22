import numpy as np
from sklearn.cluster import DBSCAN
from collections import Counter

from clustering.Cluster import Cluster
from clustering.PSOAlgorithm import PSOAlgorithm
from si.pso.CoPSO import CoPSO
from si.pso.IncreaseIWPSO import IncreaseIWPSO
from si.pso.StochasticIWPSO import StochasticIWPSO
from si.pso.DCMPSO import DCMPSO
from utils.charts import get_visual_cluster


class DCM:
    def __init__(self, clustering_method, pso_algorithm, hetnet, timestep):
        self.method = clustering_method
        self.pso_algorithm = pso_algorithm
        self.data = []
        self.optimization_output = {}
        self.ue_list = hetnet.ue_list
        self.clusters = []
        self.priority_ues_weight = hetnet.env.priority_ues_weight
        self.ordinary_ues_weight = hetnet.env.ordinary_ues_weight
        self.outage_threshold = hetnet.env.outage_threshold
        self.timestep = timestep

        # Extract UE position to a numpy array
        for ue in self.ue_list:
            self.data.append([ue.point.x, ue.point.y])
        self.data = np.array(self.data)

    # TODO: Incluir parametros na configuração DEFAULT
    def compute_clusters(self, outage_threshold=0.5, population_size=200, max_steps=150):
        # Compute clusters
        self.__optimization_engine(population_size, max_steps)
        self.__get_evaluation_per_cluster()
        self.__compute_bs_per_cluster()

    def __optimization_engine(self, population_size, max_steps):
        # TODO: Incluir parametros na configuração DEFAULT
        pso = DCMPSO(self.data, population_size, max_steps, self.method, [0.9, 0.6], [2.05, 2.05])
        pso.search()
        gbest = pso.g_best

        # Visual representation
        get_visual_cluster(gbest, self.data)

        # Generate clusters with optimized parameters
        db = DBSCAN(eps=gbest.epsilon, min_samples=gbest.min_samples).fit(self.data)
        labels = db.labels_

        counter = Counter(labels.tolist())
        grouped_labels = [[k, ]*v for k, v in counter.items()]
        label_ids = []
        for group in grouped_labels:
            if group[0] is not  -1:
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
        for cluster in self.clusters:
            print("Cluster {}".format(cluster.id))
            for ue in cluster.ue_list:
                print(ue)
            print("\n")

    def optimization_engine(self, population_size, max_steps=150):
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
