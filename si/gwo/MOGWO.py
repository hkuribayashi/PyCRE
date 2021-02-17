import random

from si.gwo.MOGWOSegmentController import MOGWOSegmentController
from si.gwo.MOGWOWolf import MOGWOWolf


class MOGWO:
    def __init__(self, max_steps, population_size, n_segments):
        self.max_steps = max_steps
        self.population = []
        self.a = []

        # Initialize the Grey Wolf population
        for idx in range(population_size):
            self.population.append(MOGWOWolf(idx))

        # Initialize a
        for step in range(max_steps):
            current_a = 2.0 * (1.0 - step / self.max_steps)
            self.a.append(current_a)

        # Calculate the fitness of each search agent
        self.evaluate()

        # Find the non-dominated solutions and initialized the archive with them
        self.segment_controller = MOGWOSegmentController(n_segments, self.population)

        # Select the alpha leader
        self.alpha, alpha_segment_id = self.segment_controller.select_leader()

        # Select the beta leader
        self.beta, beta_segment_id = self.segment_controller.select_leader()

        # Select the delta leader
        self.delta, delta_segment_id = self.segment_controller.select_leader()

        # Add back alpha, beta and delta to the archive
        self.segment_controller.add_leader(alpha_segment_id, self.alpha)
        self.segment_controller.add_leader(beta_segment_id, self.beta)
        self.segment_controller.add_leader(delta_segment_id, self.delta)

    def evaluate(self):
        for p in self.population:
            p.evaluate()

    def find_nondominated_solutions(self):
        non_dominated = []
        for idx, p in enumerate(self.population):
            if len(non_dominated) is 0:
                non_dominated.append(p)
            else:
                list_add = []
                list_del = []
                for other_p_id, other_p in enumerate(non_dominated):
                    if p < other_p:
                        # non_dominated.append(p)
                        list_add.append(p)
                        # non_dominated.remove(other_p)
                        list_del.append(other_p)
                    elif p.evaluation_f1 < other_p.evaluation_f1 or p.evaluation_f2 < other_p.evaluation_f2:
                        # non_dominated.append(p)
                        list_add.append(p)
                for id_del in list_del:
                    non_dominated.remove(id_del)
                for id_add in list_add:
                    non_dominated.append(id_add)

        return list(set(non_dominated))

    def search(self):
        counter = 0
        while counter < self.max_steps:
            print("Step: {}".format(counter))
            for p in self.population:
                # Alpha
                r1 = random.random()
                r2 = random.random()
                A = 2.0 * self.a[counter] * r1 - self.a[counter]
                C = 2.0 * r2
                D_alpha = abs(C * self.alpha.base_radius - p.base_radius)
                x1_base_radius = self.alpha.base_radius - A * D_alpha

                r1 = random.random()
                r2 = random.random()
                A = 2.0 * self.a[counter] * r1 - self.a[counter]
                C = 2.0 * r2
                D_alpha = abs(C * self.alpha.slant_height - p.slant_height)
                x1_slant_height = self.alpha.slant_height - A * D_alpha

                # Beta
                r1 = random.random()
                r2 = random.random()
                A = 2.0 * self.a[counter] * r1 - self.a[counter]
                C = 2.0 * r2
                D_beta = abs(C * self.beta.base_radius - p.base_radius)
                x2_base_radius = self.beta.base_radius - A * D_beta

                r1 = random.random()
                r2 = random.random()
                A = 2.0 * self.a[counter] * r1 - self.a[counter]
                C = 2.0 * r2
                D_beta = abs(C * self.beta.slant_height - p.slant_height)
                x2_slant_height = self.beta.slant_height - A * D_beta

                # Delta
                r1 = random.random()
                r2 = random.random()
                A = 2.0 * self.a[counter] * r1 - self.a[counter]
                C = 2.0 * r2
                D_delta = abs(C * self.delta.base_radius - p.base_radius)
                x3_base_radius = self.delta.base_radius - A * D_delta

                r1 = random.random()
                r2 = random.random()
                A = 2.0 * self.a[counter] * r1 - self.a[counter]
                C = 2.0 * r2
                D_delta = abs(C * self.delta.slant_height - p.slant_height)
                x3_slant_height = self.delta.slant_height - A * D_delta

                # Compute the mean position
                mean_base_radius = int((x1_base_radius + x2_base_radius + x3_base_radius) / 3.0)
                mean_slant_height = (x1_slant_height + x2_slant_height + x3_slant_height) / 3.0

                # Checking constrainsts
                # Base Radius Constraint
                if mean_base_radius <= 0:
                    mean_base_radius = 0.1
                elif mean_base_radius > 10:
                    mean_base_radius = 10.0

                # Slant Height Constraint
                if mean_slant_height <= 0:
                    mean_slant_height = 0.1
                elif mean_slant_height > 20:
                    mean_slant_height = 20.0

                p.base_radius = mean_base_radius
                p.slant_height = mean_slant_height

            # Calculate the objective values of all search agents
            self.evaluate()

            # Find the non-dominated solutions
            non_dominated_list = self.find_nondominated_solutions()

            # Update the archive with respect to the obtained non-dominated solutions
            self.segment_controller.update(non_dominated_list)

            # Select the alpha leader
            temp_alpha, alpha_segment_id = self.segment_controller.select_leader()
            if temp_alpha < self.alpha:
                self.alpha = temp_alpha

            # Select the beta leader
            temp_beta, beta_segment_id = self.segment_controller.select_leader()
            if temp_beta < self.beta:
                self.beta = temp_beta

            # Select the delta leader
            temp_delta, delta_segment_id = self.segment_controller.select_leader()
            if temp_delta < self.delta:
                self.delta = temp_delta

            # Add back alpha, beta and delta to the archive
            self.segment_controller.add_leader(alpha_segment_id, temp_alpha)
            self.segment_controller.add_leader(beta_segment_id, temp_beta)
            self.segment_controller.add_leader(delta_segment_id, temp_delta)

            counter += 1

    def get_archive(self):
        for key in self.segment_controller.segments:
            print("Segment ID: {}".format(key))
            for p in self.segment_controller.segments[key].archive:
                print(p)