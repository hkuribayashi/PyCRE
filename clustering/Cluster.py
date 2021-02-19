import numpy as np


class Cluster:

    def __init__(self, id_, env):
        self.id = id_
        self.ue_list = []
        self.evaluation = {}
        self.env = env
        self.target_cluster = False

    def evaluate(self):
        fulfilled_qos_ues = np.array([ue for ue in self.ue_list if ue.evaluation is True])
        weighted_sum = 0
        for ue in fulfilled_qos_ues:
            if ue.priority:
                weighted_sum += self.env.priority_ues_weight
            else:
                weighted_sum += self.env.ordinary_ues_weight
        total_weights = self.ueQueue.total_priority_ues * self.env.priority_ues_weight + \
                        self.ueQueue.total_ordinary_ues * self.env.ordinary_ues_weight
        self.evaluation['satisfaction'] = (weighted_sum / total_weights) * 100
        self.evaluation['total_ue'] = len(self.ue_list)
        self.evaluation['total_priority_ues'] = self.ueQueue.total_priority_ues
        self.evaluation['total_ordinary_ues'] = self.ueQueue.total_ordinary_ues
