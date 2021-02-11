import numpy as np

from si.pso.PSO import PSO
from utils.charts import get_evaluation_evolution


class DCM:
    def __init__(self, method, ue_list):
        self.method = method
        self.data = []
        self.optimization_output = {}

        # Extract UE position to a numpy array
        for ue in ue_list:
            self.data.append([ue.point.x, ue.point.y])
        self.data = np.array(self.data)

    def optimization_engine(self):
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
