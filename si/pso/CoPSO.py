import random
import numpy as np
from operator import attrgetter

from si.pso.CoPSOParticle import CoPsoParticle


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

        self.pool.close()
        self.pool.join()

    def update_position(self, particle, constriction_factor):
        phi1 = random.random()
        phi2 = random.random()

        # Update epsilon velocity
        velocity_epsilon = (particle.best_epsilon - particle.epsilon) * phi1 * 2.05 + \
                           (self.g_best.best_epsilon - particle.epsilon) * phi2 * 2.05

        # Update epsilon position
        particle.epsilon = constriction_factor * (particle.epsilon + velocity_epsilon)

        # Epsilon Constraint
        if particle.epsilon < 0:
            particle.epsilon = 0.1

        # Update Min samples velocity
        velocity_min_samples = (particle.best_min_samples - particle.min_samples) * phi1 + \
                               (self.g_best.best_min_samples - particle.min_samples) * phi2

        # Update Min samples position
        particle.min_samples = int(constriction_factor * (particle.min_samples + velocity_min_samples))

        # Min Samples Constraint
        if particle.min_samples < 2:
            particle.min_samples = 2
        elif particle.min_samples > particle.data_size:
            particle.min_samples = particle.data_size - 1
