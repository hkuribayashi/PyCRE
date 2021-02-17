import random

from si.gwo.GWOWolf import Wolf


class GWO:
    def __init__(self, data, max_steps, population_size):
        self.max_steps = max_steps
        self.population = []
        self.data = data
        self.a = []
        self.global_evaluation = []
        self.best_evaluation = []

        # Initialize the Grey Wolf population
        for idx in range(population_size):
            self.population.append(Wolf(len(self.data)))

        # Initialize a
        for step in range(max_steps):
            current_a = 2.0 * (1.0 - step/self.max_steps)
            self.a.append(current_a)

        # Calculate the fitness of each search agent
        self.evaluate()

        # Sort the wolf pack and select the wolf leaders
        self.population.sort(key=lambda x: x.evaluation, reverse=False)
        self.alpha = Wolf(len(self.data))
        self.alpha.min_samples = self.population[0].min_samples
        self.alpha.epsilon = self.population[0].epsilon
        self.alpha.evaluation = self.population[0].evaluation

        self.beta = Wolf(len(self.data))
        self.beta.min_samples = self.population[1].min_samples
        self.beta.epsilon = self.population[1].epsilon
        self.beta.evaluation = self.population[1].evaluation

        self.delta = Wolf(len(self.data))
        self.delta.min_samples = self.population[2].min_samples
        self.delta.epsilon = self.population[2].epsilon
        self.delta.evaluation = self.population[2].epsilon
        self.delta.evaluation = self.population[2].epsilon

    def evaluate(self):
        # Initialize aux variable
        sum_temp = 0

        # Sum each each particle evaluation
        for p in self.population:
            p.evaluate(self.data)
            sum_temp += p.evaluation

        # Compute the mean evaluation
        return sum_temp/len(self.population)

    def search(self):
        counter = 0
        while counter < self.max_steps:

            for p in self.population:
                if p.evaluation < self.alpha.evaluation:
                    self.alpha.evaluation = p.evaluation
                    self.alpha.min_samples = p.min_samples
                    self.alpha.epsilon = p.epsilon
                elif p.evaluation < self.beta.evaluation:
                    self.beta.evaluation = p.evaluation
                    self.beta.min_samples = p.min_samples
                    self.beta.epsilon = p.epsilon
                elif p.evaluation < self.delta.evaluation:
                    self.delta.evaluation = p.evaluation
                    self.delta.min_samples = p.min_samples
                    self.delta.epsilon = p.epsilon

            for p in self.population:
                # Alpha
                r1 = random.random()
                r2 = random.random()
                A = 2.0 * self.a[counter] * r1 - self.a[counter]
                C = 2.0 * r2
                D_alpha = abs(C * self.alpha.min_samples - p.min_samples)
                X1_min_samples = self.alpha.min_samples - A * D_alpha

                r1 = random.random()
                r2 = random.random()
                A = 2.0 * self.a[counter] * r1 - self.a[counter]
                C = 2.0 * r2
                D_alpha = abs(C * self.alpha.epsilon - p.epsilon)
                X1_epsilon = self.alpha.epsilon - A * D_alpha

                # Beta
                r1 = random.random()
                r2 = random.random()
                A = 2.0 * self.a[counter] * r1 - self.a[counter]
                C = 2.0 * r2
                D_beta = abs(C * self.beta.min_samples - p.min_samples)
                X2_min_samples = self.beta.min_samples - A * D_beta

                r1 = random.random()
                r2 = random.random()
                A = 2.0 * self.a[counter] * r1 - self.a[counter]
                C = 2.0 * r2
                D_beta = abs(C * self.beta.epsilon - p.epsilon)
                X2_epsilon = self.beta.epsilon - A * D_beta

                # Delta
                r1 = random.random()
                r2 = random.random()
                A = 2.0 * self.a[counter] * r1 - self.a[counter]
                C = 2.0 * r2
                D_delta = abs(C * self.delta.min_samples - p.min_samples)
                X3_min_samples = self.delta.min_samples - A * D_delta

                r1 = random.random()
                r2 = random.random()
                A = 2.0 * self.a[counter] * r1 - self.a[counter]
                C = 2.0 * r2
                D_delta = abs(C * self.delta.epsilon - p.epsilon)
                X3_epsilon = self.delta.epsilon - A * D_delta

                # Compute the mean position
                mean_min_samples = int((X1_min_samples + X2_min_samples + X3_min_samples)/3.0)
                mean_episilon = (X1_epsilon + X2_epsilon + X3_epsilon)/3.0

                # Checking constrainsts
                # Min Samples Constraint
                if mean_min_samples < 2:
                    mean_min_samples = 2
                elif mean_min_samples > len(self.data):
                    mean_min_samples = len(self.data) - 1

                # Epsilon Constraint
                if mean_episilon < 0:
                    mean_episilon = 0.1

                p.min_samples = mean_min_samples
                p.epsilon = mean_episilon

            # Get global mean evaluation
            evaluation = self.evaluate()
            self.global_evaluation.append(evaluation)

            # Get the best evaluation
            best_evaluation = self.alpha.evaluation
            self.best_evaluation.append(best_evaluation)

            print('Iteration {} - Mean Evaluation: {} | Alpha Evaluation: {}'.format(counter, evaluation, best_evaluation))

            counter += 1
