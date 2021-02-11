import numpy as np

class Flower:

    def __init__(self, dimensions):
        self.current_solution = np.random.uniform(low=-100.0, high=100.0, size=(dimensions,))
        self.best_solution = None
        self.evaluation = -500.0
        self.result = None

    def evaluate(self):
        evaluation = 0
        for x in self.current_solution:
            evaluation += x ** 2
        self.evaluation = evaluation