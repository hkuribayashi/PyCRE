import random
import numpy as np
from functools import total_ordering


# Min lateral surface area
def objective_f1(base_radius, slant_height):
    return np.pi * base_radius * np.sqrt(base_radius ** 2 + slant_height ** 2)


# Min total area
def objective_f2(base_radius, slant_height):
    return np.pi * base_radius * (base_radius + np.sqrt(base_radius ** 2 + slant_height ** 2))


# Constraint Verification
def constraint_verification(base_radius, slant_height):
    if base_radius < 0 or base_radius > 10:
        return False
    elif slant_height < 0 or slant_height > 20:
        return False
    else:
        return True


class MOGWOWolf:
    def __init__(self, idx):
        self.idx = idx
        self.base_radius = random.randint(1, 10)
        self.slant_height = random.randint(1, 20)
        self.evaluation_f1 = float('inf')
        self.evaluation_f2 = float('inf')
        self.volume = 0.0

    def __hash__(self):
        return self.idx

    def evaluate(self):
        self.volume = (np.pi / 3.0) * (self.base_radius ** 2) * self.slant_height
        if constraint_verification(self.base_radius, self.slant_height):
            self.evaluation_f1 = objective_f1(self.base_radius, self.slant_height)
            self.evaluation_f2 = objective_f2(self.base_radius, self.slant_height)
        else:
            self.evaluation_f1 = float('inf')
            self.evaluation_f2 = float('inf')

    def __eq__(self, other):
        if isinstance(other, MOGWOWolf):
            return self.idx == other.idx
        return False

    def __str__(self):
        return "[MOGWOWolf id={}, base_radius={}, slant_height={}, evaluation_f1={}, evaluation_f2={}, volume={}]".format(
            self.idx, self.base_radius, self.slant_height, self.evaluation_f1, self.evaluation_f2, self.volume)

    @total_ordering
    def __lt__(self, other):
        return self.evaluation_f1 < other.evaluation_f1 and self.evaluation_f2 < other.evaluation_f2
