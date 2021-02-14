import random

from si.pso.PSOParticle import Particle


class IncreaseIWParticle(Particle):

    def __init__(self, clustering_method, data_size, cognitive_factor):
        super().__init__(clustering_method, data_size, cognitive_factor)
