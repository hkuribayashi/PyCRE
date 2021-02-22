from infrastructure.GWOAlgorithm import GWOAlgorithm
from si.gwo.GWO import GWO
from si.gwo.MOGWO import MOGWO


class IOM:

    def __init__(self, cluster, optimization_strategy):
        self.cluster = cluster
        self.optimization_strategy = optimization_strategy
        self.optimization_output = {}

    def __optimization_engine(self, population_size, max_steps, segments):
        if self.optimization_strategy is GWOAlgorithm.GWO:
            gwo = GWO(self.cluster, max_steps, population_size)
            gwo.search()
            self.optimization_output['GWO-{}'.format(population_size)] = ""
            self.optimization_output['GWO-{}-gbest'.format(population_size)] = ""
        elif self.optimization_strategy is GWOAlgorithm.MOGWO:
            mogwo = MOGWO(self.cluster, max_steps, population_size, segments)
            mogwo.search()
            self.optimization_output['MOGWO-{}'.format(population_size)] = ""

    def compute_network_slice(self, population_size=100, max_steps=200, segments=10):
        self.__optimization_engine(population_size, max_steps,segments)