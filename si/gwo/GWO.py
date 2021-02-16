import random

from si.gwo.Wolf import Wolf


class GWO:
    def __init__(self, data, max_steps, population_size):
        self.max_steps = max_steps
        self.population = []
        self.data = data
        self.a = []
        self.global_evaluation = None

        # Initialize the Grey Wolf population
        for idx in range(population_size):
            self.population.append(Wolf(len(self.data)))

        # Initialize a
        for step in range(max_steps):
            current_a = 2.0 * (1.0 - step/self.max_steps)
            self.a.append(current_a)

        # Initialize A and C
        self.C = []
        self.A = []
        for a_ in self.a:
            r1 = random.random()
            self.C.append(2.0 * r1)
            r2 = random.random()
            self.A.append(2.0 * a_ * r2 - a_)

        # Calculate the fitness of each search agent
        self.evaluate()

        # Select the wolf leaders
        self.alpha, self.beta, self.delta = self.select_leaders()

    def select_leaders(self):
        # Sort the wolf pack
        self.population.sort(key=lambda x: x.evaluation, reverse=True)
        return self.population[0], self.population[1], self.population[2]

    def evaluate(self):
        # Initialize aux variable
        sum_temp = 0

        # Sum each each particle evaluation
        for p in self.population:
            p.evaluate(self.data)
            sum_temp += p.evaluation

        # Compute the mean evaluation
        return sum_temp/len(self.population)

    def seaerch(self):
        counter = 0
        while counter < self.max_steps:

            # Compute the mean position
            mean_min_samples = int((self.alpha.min_samples + self.beta.min_samples + self.delta.min_samples)/3.0)
            mean_episilon = (self.alpha.epsilon + self.beta.epsilon + self.delta.epsilon)/3.0

            # Checking constrainsts
            # Min Samples Constraint
            if mean_min_samples < 2:
                mean_min_samples = 2
            elif mean_min_samples > len(self.data):
                mean_min_samples = len(self.data) - 1

            # Epsilon Constraint
            if mean_episilon < 0:
                mean_episilon = 0.1

            # Update the position of each search agent
            for p in self.population:
                p.update_position(mean_min_samples, mean_episilon)

            # Get global mean evaluation
            self.global_evaluation.append(self.evaluate())

            # Update alpha, beta and delta wolves
            self.select_leaders()

            counter += 1
