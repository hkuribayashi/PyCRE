from operator import attrgetter

from si.pso.DCMPSOParticle import DCMPSOParticle
from si.pso.PSO import PSO


class DCMPSO(PSO):

    def __init__(self, data, population_size, max_steps, clustering_method, inertia_weight, cognitive_factor):
        super().__init__(data, max_steps, clustering_method)
        self.inertia_weight = []
        self.mean_evaluation_evolution = []
        self.gbest_evaluation_evolution = []
        self.last_evaluation = 1.0
        self.cognitive_factor = cognitive_factor

        # Create the PSO population
        for i in range(population_size):
            self.population.append(DCMPSOParticle(self.clustering_method, len(self.data), cognitive_factor))

        # Initialize the inertia weight list
        initial_inertia = inertia_weight[0]
        final_inertia = inertia_weight[1]
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
        print("Starting DCMPSO Engine with {} particles and {} iterations".format(len(self.population), self.max_steps))
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
                    p = DCMPSOParticle(self.clustering_method, len(self.data), self.cognitive_factor)
                    p.evaluate(self.data)
                    self.population.append(p)

            # Update the particles' position
            for p in self.population:
                p.update_position(self.g_best, self.inertia_weight[counter])

            # Save current mean evaluation and gbest evaluation
            self.mean_evaluation_evolution.append(self.global_evaluation)
            self.gbest_evaluation_evolution.append(self.g_best.evaluation)

            print('Iteration {} - Mean Evaluation: {} | Gbest Evaluation: {}'.format(counter, self.global_evaluation, self.g_best.evaluation))

            counter += 1
