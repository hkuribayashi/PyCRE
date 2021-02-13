import numpy as np
from operator import attrgetter

from si.pso.CoPsoParticle import CoPsoParticle


class CoPSO:

    def __init__(self, data, population_size, max_steps, clustering_method):
        self.population = list()
        self.g_best = None
        self.global_evaluation = 1
        self.max_steps = max_steps
        self.data = data
        self.clustering_method = clustering_method
        self.mean_evaluation_evolution = []
        self.gbest_evaluation_evolution = []
        self.constricion_factor = None

        # Create the PSO population
        for i in range(population_size):
            self.population.append(CoPsoParticle(self.clustering_method, len(self.data)))

        # Constriction Factor Parameter
        c = 2.05 + 2.05

        # Computing the constriction factor value
        self.constricion_factor = 2.0/(np.abs(2 - c - np.sqrt((c**2) - 4*c)))

    def evaluate(self):
        # Initialize aux variable
        sum_temp = 0

        # Sum each each particle evaluation
        for p in self.population:
            p.evaluate(self.data)
            sum_temp += p.evaluation

        # Compute the mean evaluation
        self.global_evaluation = sum_temp/len(self.population)

        # Get the best particle
        self.g_best = min(self.population, key=attrgetter('evaluation'))

    def search(self):
        counter = 0
        while counter < self.max_steps:
            # Evaluate the population
            self.evaluate()

            # Update the particles' position
            for p in self.population:
                p.update_position(self.g_best, self.constricion_factor)

            # Save current mean evaluation
            print('Step {}: Mean Evaluation {}'.format(counter, self.global_evaluation))
            self.mean_evaluation_evolution.append(self.global_evaluation)

            # Save current gbest evaluation
            print('Step {}: GBest Evaluation {}'.format(counter, self.g_best.evaluation))
            self.gbest_evaluation_evolution.append(self.g_best.evaluation)

            # Increase the iteration counter
            counter += 1
