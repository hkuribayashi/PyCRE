import math
import random
import numpy as np
from si.fpa.flower import Flower
from operator import attrgetter


class FPA:

    def __init__(self, population_size, max_steps, dimensions):
        self.g_best = None
        self.dimensions = dimensions
        self.population = list()
        self.switch_probability = 0
        self.max_steps = max_steps
        for i in range(population_size):
            self.population.append(Flower(dimensions))

    def evaluate(self):
        # Evaluate each particle
        for f in self.population:
            f.evaluate()

        # Get the best particle
        self.g_best = max(self.population, key=attrgetter('evaluation'))

    def get_levy(self, _lambda):
        left_side = math.gamma(1 + _lambda)/(_lambda * math.gamma((1 + _lambda)/2))
        right_side = np.sin(np.pi * _lambda/2)/2**((_lambda - 1)/2)
        sigma_u = (left_side * right_side)**(1/_lambda)
        sigma_v = 1
        U = np.zeros(self.dimensions)
        V = np.zeros(self.dimensions)
        for i in range(self.dimensions):
            U[i] = np.random.gamma(0, sigma_u)
            V[i] = np.random.gamma(0, sigma_v)

    def search(self):
        counter = 0
        self.switch_probability = 0.8
        while counter < self.max_steps:
            for f in self.population:
                if random.uniform(0, 1) < self.switch_probability:
                    # Draw a d-dimensional step vector L which obeys a L'vey distribution

                else:
                    # Draw u from a uniform distribution in [0,1]
                    print()
                self.evaluate()
