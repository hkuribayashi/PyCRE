from operator import attrgetter
from si.pso.particle import Particle


class PSO:

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

        # Create the PSO population
        for i in range(population_size):
            self.population.append(Particle(self.clustering_method, len(self.data)))

        # Initialize the inertia weight list
        initial_inertia = 0.9
        final_inertia = 0.6
        for step in range(max_steps):
            current_inertia = initial_inertia + ((step/max_steps)*(final_inertia - initial_inertia))
            self.inertia_weight.append(current_inertia)

    def evaluate(self):
        # Initialize aux variable
        sum_temp = 0

        # Sum each each particle evaluation
        for p in self.population:
            p.evaluate(self.data)
            sum_temp += p.evaluation

        # Compute the mean evaluation
        current_global_evaluation = sum_temp/len(self.population)

        # Get the best particle
        self.g_best = min(self.population, key=attrgetter('evaluation'))

        return current_global_evaluation

    def search(self):
        counter = 0
        k = 0
        while counter < self.max_steps:
            current_global_evaluation = self.evaluate()
            # TODO: Incluir parâmetro 0.001 na Configuração DEFAULT
            if abs(current_global_evaluation - self.last_evaluation) < 0.001:
                k += 1

            # Update the variables
            self.global_evaluation = current_global_evaluation
            self.last_evaluation = current_global_evaluation

            # Replace part of the population which is below the mean evaluation
            # TODO: Incluir parâmetro k na Configuração DEFAULT
            if k == 15:
                k = 0
                # counter -= 5
                selected_population = [p for p in self.population if p.evaluation <= current_global_evaluation]
                size_excluded = len(self.population) - len(selected_population)
                self.population = selected_population
                for i in range(size_excluded):
                    p = Particle(self.clustering_method, len(self.data))
                    p.evaluate(self.data)
                    self.population.append(p)

            # Update the particles' position
            for p in self.population:
                p.update_position(self.g_best, self.inertia_weight[counter])

            counter += 1
            # Save current mean evaluation
            print('Step {}: Mean Evaluation {}'.format(counter, self.global_evaluation))
            self.mean_evaluation_evolution.append(self.global_evaluation)

            # Save current gbest evaluation
            print('Step {}: GBest Evaluation {}'.format(counter, self.g_best.evaluation))
            self.gbest_evaluation_evolution.append(self.g_best.evaluation)
