import copy
import random
import numpy as np

from si.gwo.MOGWOSegmentController import MOGWOSegmentController
from si.gwo.MOGWOWolf import MOGWOWolf


def find_nondominated_solutions(populacao):
    non_dominated_list = [copy.deepcopy(populacao[0])]

    for p in populacao:
        non_dominated_list = list(set(non_dominated_list))
        list_del = []
        flag = False
        for non_dominated in non_dominated_list:
            if p <= non_dominated:
                flag = True
                list_del.append(non_dominated)
            elif p.evaluation_f1 <= non_dominated.evaluation_f1 or p.evaluation_f2 <= non_dominated.evaluation_f2:
                flag = True
            else:
                flag = False
        for element in list_del:
            non_dominated_list.remove(element)
        if flag:
            non_dominated_list.append(copy.deepcopy(p))

    return list(set(non_dominated_list))


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

        # Find the non-dominated solutions
        non_dominatead_solutions_set = []
        for seg in range(n_segments):
            population_ = []
            for idx in range(population_size):
                p_ = MOGWOWolf(idx)
                p_.evaluate()
                population_.append(p_)
            non_dominatead_solutions = find_nondominated_solutions(population_)
            non_dominatead_solutions_set.append(non_dominatead_solutions)

        # Initialize the archive with the non-dominated solutions
        self.segment_controller = MOGWOSegmentController(n_segments, non_dominatead_solutions_set)

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
                    mean_base_radius = 0.001
                elif mean_base_radius > 10:
                    mean_base_radius = 10.0

                # Slant Height Constraint
                if mean_slant_height <= 0:
                    mean_slant_height = 0.001
                elif mean_slant_height > 20:
                    mean_slant_height = 20.0

                p.base_radius = mean_base_radius
                p.slant_height = mean_slant_height

            # Calculate the objective values of all search agents
            self.evaluate()

            # Find the non-dominated solutions
            non_dominated_list = find_nondominated_solutions(self.population)

            # Update the archive with respect to the obtained non-dominated solutions
            self.segment_controller.update(non_dominated_list)

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

            counter += 1

    def get_archive(self):
        for key in self.segment_controller.segments:
            print("Segment ID: {}".format(key))
            for p in self.segment_controller.segments[key].archive:
                print(p)
        print("\n")
        for key in self.segment_controller.segments:
            print("Segment ID: {}".format(key))
            for p in self.segment_controller.segments[key].archive:
                p.evaluate()
                print(p)
                print (np.pi * p.base_radius * np.sqrt(p.base_radius ** 2 + p.slant_height ** 2))