import numpy as np

from mobility.point import Point
from network.ue import UE


class SimpleQueue:
    def __init__(self, arrival_rate, service_rate, total_time, simulation_rea, ue_height):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.total_time = total_time
        self.total_ues = []
        self.ues = []
        self.dimension = np.math.sqrt(simulation_rea)
        self.ue_height = ue_height

        for i in range(self.total_time):
            self.total_ues.append(i * self.arrival_rate)

        for i in range(2, self.total_time):
            self.total_ues[i] = self.total_ues[i] - (i - 1) * self.service_rate

        self.__populate_ues()

    def __populate_ues(self):
        for idx, total in enumerate(self.total_ues):
            ue_list = []
            if idx > 0:
                new_ues = total - self.total_ues[idx - 1]
            else:
                new_ues = total
            total_priority = 1
            counter_priority = total_priority
            for i in range(new_ues):
                x = np.random.randint(self.dimension * (-1), self.dimension)
                y = np.random.randint(self.dimension * (-1), self.dimension)
                p_i = Point(x, y, self.ue_height)
                ue = UE(i, p_i)
                if total_priority > 0 and counter_priority > 0:
                    ue.priority = True
                    counter_priority = counter_priority - 1
                ue_list.append(ue)
            self.ues.append(ue_list)

    def __str__(self):
        return '[arrival_rate={}, service_rate={}]'.format(self.arrival_rate, self.service_rate)
