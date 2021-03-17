import numpy as np
from itertools import chain

from infrastructure.GWOAlgorithm import GWOAlgorithm
from infrastructure.Slice import Slice
from si.gwo.GWO import GWO
from si.gwo.MOGWO import MOGWO
from utils.charts import get_visual_pareto
from utils.misc import save_to_csv


class IOM:

    def __init__(self, cluster, path):
        self.cluster = cluster
        self.path = path
        self.best_solution = {}

    def __optimization_engine(self, optimization_strategy, population_size, max_steps, segments, simulations, pareto_weight=None):
        global_evolution = []
        alpha_evolution = []
        if optimization_strategy is GWOAlgorithm.GWO:
            counter = 0
            best_evaluation = np.NINF
            while counter < simulations:
                gwo = GWO(self.cluster, max_steps, population_size, pareto_weight)
                gwo.search()
                global_evolution.append(gwo.global_evaluation)
                alpha_evolution.append(gwo.best_evaluation)
                if gwo.alpha.evaluation > best_evaluation:
                    best_evaluation = gwo.alpha.evaluation
                    gwo.alpha.adjust_position()
                    self.best_solution[pareto_weight] = gwo.alpha.solution.copy()
                counter += 1
        elif optimization_strategy is GWOAlgorithm.MOGWO:
            counter = 0
            while counter < simulations:
                mogwo = MOGWO(self.cluster, max_steps, population_size, segments)
                mogwo.search()
                global_evolution.append(mogwo.archive)
                counter += 1

        return global_evolution, alpha_evolution

    def compute_network_slice(self, id_, user_density, optimization_strategy, pop_size=200, max_steps=300, segments=10, simulations=5):
        global result
        if len(self.cluster.bs_list) == 1:
            result = Slice(self.cluster, None)
        elif optimization_strategy is GWOAlgorithm.GWO:
            for weight in reversed(range(1, 10)):
                weight = weight/10
                global_evolution, alpha_evolution = self.__optimization_engine(optimization_strategy, pop_size, max_steps, segments, simulations, weight)
                save_to_csv(global_evolution, self.path, "iom_{}_cluster_mean_evolution_{}_pop_{}_GWO_{}.csv".format(user_density,weight, pop_size, id_))
                save_to_csv(alpha_evolution, self.path, "iom_{}_cluster_mean_evolution_{}_pop_{}_GWO_alpha-{}.csv".format(user_density, weight, pop_size, id_))
            result = Slice(self.cluster, self.best_solution)
        elif optimization_strategy is GWOAlgorithm.MOGWO:
            global_evolution, _ = self.__optimization_engine(optimization_strategy, pop_size, max_steps, segments, simulations)
            flatten_list = list(chain.from_iterable(global_evolution))
            flatten_list = list(chain.from_iterable(flatten_list))
            get_visual_pareto(flatten_list)
            result = Slice(self.cluster, flatten_list)
        return result
