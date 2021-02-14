import numpy as np

from clustering.PSOAlgorithm import PSOAlgorithm
from si.pso.CoPSO import CoPSO
from si.pso.IncreaseIWPSO import IncreaseIWPSO
from si.pso.StochasticIWPSO import StochasticIWPSO
from si.pso.DCMPSO import DCMPSO


class DCM:
    def __init__(self, clustering_method, pso_algorithm, ue_list):
        self.method = clustering_method
        self.pso_algorithm = pso_algorithm
        self.data = []
        self.optimization_output = {}

        # Extract UE position to a numpy array
        for ue in ue_list:
            self.data.append([ue.point.x, ue.point.y])
        self.data = np.array(self.data)

    # TODO: Incluir parametros na configuração DEFAULT
    def optimization_engine(self, population_size, max_steps=150):
        if self.pso_algorithm is PSOAlgorithm.DCMPSO:
            pso = DCMPSO(self.data, population_size, max_steps, self.method, [0.9, 0.6], [2.05, 2.05])
            pso.search()
            self.optimization_output = {'DCMPSO-DCM-{}'.format(population_size): pso.mean_evaluation_evolution,
                                        'DCMPSO-DCM-{}-gbest'.format(population_size): pso.gbest_evaluation_evolution}
        elif self.pso_algorithm is PSOAlgorithm.CoPSO:
            pso = CoPSO(self.data, population_size, max_steps, self.method, [2.05, 2.05])
            pso.search()
            self.optimization_output = {'CoPSO-DCM-{}'.format(population_size): pso.mean_evaluation_evolution,
                                        'CoPSO-DCM-{}-gbest'.format(population_size): pso.gbest_evaluation_evolution}
        elif self.pso_algorithm is PSOAlgorithm.IncreaseIWPSO:
            pso = IncreaseIWPSO(self.data, population_size, max_steps, self.method, [0.4, 0.9], [2.0, 2.0])
            pso.search()
            self.optimization_output = {'IIWPSO-DCM-{}'.format(population_size): pso.mean_evaluation_evolution,
                                        'IIWPSO-DCM-{}-gbest'.format(population_size): pso.gbest_evaluation_evolution}
        elif self.pso_algorithm is PSOAlgorithm.StochasticIWPSO:
            pso = StochasticIWPSO(self.data, population_size, max_steps, self.method)
            pso.search()
            self.optimization_output = {'SIWPSO-DCM-{}'.format(population_size): pso.mean_evaluation_evolution,
                                        'SIWPSO-DCM-{}-gbest'.format(population_size): pso.gbest_evaluation_evolution}
