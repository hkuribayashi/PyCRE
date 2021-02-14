import numpy as np

from clustering.PSOAlgorithm import PSOAlgorithm
from si.pso.CoPSO import CoPSO
from si.pso.IncreaseIWPSO import IncreaseIWPSO
from si.pso.PSO import PSO
from si.pso.StochasticIWPO import StochasticIWPSO


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

    def optimization_engine(self):
        if self.pso_algorithm is PSOAlgorithm.DCMPSO:
            # TODO: Incluir parâmetros na Configuração DEFAULT
            pso50 = PSO(self.data, 50, 150, self.method)
            pso50.search()

            pso100 = PSO(self.data, 100, 150, self.method)
            pso100.search()

            pso200 = PSO(self.data, 200, 150, self.method)
            pso200.search()

            self.optimization_output = {'PSO-DCM-50': pso50.mean_evaluation_evolution,
                                        'PSO-DCM-50-gbest': pso50.gbest_evaluation_evolution,
                                        'PSO-DCM-100': pso100.mean_evaluation_evolution,
                                        'PSO-DCM-100-gbest': pso100.gbest_evaluation_evolution,
                                        'PSO-DCM-200': pso200.mean_evaluation_evolution,
                                        'PSO-DCM-200-gbest': pso200.gbest_evaluation_evolution}
        elif self.pso_algorithm is PSOAlgorithm.CoPSO:
            # TODO: Incluir parâmetros na Configuração DEFAULT
            pso200 = CoPSO(self.data, 200, 150, self.method)
            pso200.search()

            self.optimization_output = {'CoPSO-DCM-200': pso200.mean_evaluation_evolution,
                                        'CoPSO-DCM-200-gbest': pso200.gbest_evaluation_evolution}
        elif self.pso_algorithm is PSOAlgorithm.IncreaseIWPSO:
            # TODO: Incluir parâmetros na Configuração DEFAULT
            pso200 = IncreaseIWPSO(self.data, 200, 150, self.method)
            pso200.search()

            self.optimization_output = {'IncreaseIWPSO-DCM-200': pso200.mean_evaluation_evolution,
                                        'IncreaseIWPSO-DCM-200-gbest': pso200.gbest_evaluation_evolution}
        else:
            # TODO: Incluir parâmetros na Configuração DEFAULT
            pso200 = StochasticIWPSO(self.data, 200, 150, self.method)
            pso200.search()

            self.optimization_output = {'StochasticIWPSO-DCM-200': pso200.mean_evaluation_evolution,
                                        'StochasticIWPSO-DCM-200-gbest': pso200.gbest_evaluation_evolution}
