from operator import attrgetter
import multiprocessing as mp
from random import random

from si.pso.particle import Particle


class StochasticIWPSO:

    def __init__(self, data, population_size, max_steps, clustering_method):
        self.population = list()
        self.g_best = None
        self.global_evaluation = 1
        self.last_evaluation = 1
        self.max_steps = max_steps
        self.data = data
        self.clustering_method = clustering_method
        self.inertia_weight = []
        self.mean_evaluation_evolution = []
        self.gbest_evaluation_evolution = []
        self.pool = mp.Pool(mp.cpu_count())

        # Create the PSO population
        for i in range(population_size):
            self.population.append(Particle(self.clustering_method, len(self.data)))

        # Initialize the inertia weight list
        for step in range(max_steps):
            self.inertia_weight.append(random.uniform(0.5, 1.0))

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
                # p.update_position(self.g_best, self.inertia_weight[counter])
                self.pool.apply(p.update_position, args=(self.g_best, self.inertia_weight[counter]))

            # Save current mean evaluation
            print('Step {}: Mean Evaluation {}'.format(counter, self.global_evaluation))
            self.mean_evaluation_evolution.append(self.global_evaluation)

            # Save current gbest evaluation
            print('Step {}: GBest Evaluation {}'.format(counter, self.g_best.evaluation))
            self.gbest_evaluation_evolution.append(self.g_best.evaluation)

            counter += 1

        self.pool.close()
        self.pool.join()
