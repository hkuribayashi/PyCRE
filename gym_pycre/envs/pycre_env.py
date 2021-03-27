import gym
import copy
import numpy as np
from gym import spaces

class PyCREEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, **kwargs):
        super(PyCREEnv, self).__init__()
        self.network_slice = kwargs["network_slice"]
        self.working_slice = copy.deepcopy(kwargs["network_slice"])
        self.priority_ues_weight = self.working_slice.cluster.bs_list[-1].hetnet.env.priority_ues_weight
        self.ordinary_ues_weight = self.working_slice.cluster.bs_list[-1].hetnet.env.ordinary_ues_weight
        self.current_state = int(self.working_slice.cluster.evaluation["satisfaction"])
        self.reward_range = (-100, 10000)
        self.action_space = spaces.Discrete(len(self.working_slice.selected_bs) * 7)
        self.observation_space = spaces.Discrete(101)

    def step(self, action):
        int_action = np.int16(action).item()

        total_actions = int_action + 1
        int_part = total_actions // 7
        remainder = total_actions % 7

        if int_part > 0:
            bs_index = int_part - 1
        else:
            bs_index = 0

        if remainder == 0:
            new_action = 6
        else:
            new_action = remainder - 1

        target_bs = self.working_slice.selected_bs[bs_index]
        if target_bs.load == target_bs.max_load:
            full_flag = True
        else:
            full_flag = False

        if new_action == 0:
            target_bs.increase_bias(30.0)
        elif new_action == 1:
            target_bs.increase_bias(20.0)
        elif new_action == 2:
            target_bs.increase_bias(10.0)
        elif new_action == 3:
            target_bs.maintain_bias()
        elif new_action == 4:
            target_bs.increase_bias(-5.0)
        elif new_action == 5:
            target_bs.decrease_bias(-10.0)
        elif new_action == 6:
            target_bs.decrease_bias(-15.0)

        target_bs.hetnet.run(first_run_flag=False)
        info = dict()
        info["satisfaction"] = self.compute_satisfaction()
        new_state = int(info["satisfaction"])

        if new_state >= 75 or full_flag:
            done = True
        else:
            done = False

        if new_state >= 90 or full_flag:
            reward = 20.0
        elif new_state > self.current_state:
            reward = 1.01
        elif new_state < self.current_state:
            reward = -2.01
        else:
            reward = 0.0

        return new_state, reward, done, info

    def reset(self):
        self.working_slice = copy.deepcopy(self.network_slice)
        state = int(self.working_slice.cluster.evaluation['satisfaction'])
        return state

    def render(self, mode='human', close=False):
        pass

    def compute_satisfaction(self):
        fulfilled_qos_ues = np.array([ue for ue in self.working_slice.cluster.ue_list if ue.evaluation is True])
        total_priority_ues = len([ue for ue in self.working_slice.cluster.ue_list if ue.priority is True])
        total_ordinary_ues = len([ue for ue in self.working_slice.cluster.ue_list if ue.priority is False])

        weighted_sum = 0
        for ue in fulfilled_qos_ues:
            if ue.priority:
                weighted_sum += self.priority_ues_weight
            else:
                weighted_sum += self.ordinary_ues_weight
        total_weights = total_priority_ues * self.priority_ues_weight + total_ordinary_ues * self.ordinary_ues_weight

        return (weighted_sum / total_weights) * 100
