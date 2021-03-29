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
        self.action_space = spaces.Discrete(len(self.working_slice.selected_bs) * 9)
        self.observation_space = spaces.Discrete(101)

    def step(self, action):
        int_action = np.int16(action).item()

        total_actions = int_action + 1
        int_part = total_actions // 9
        remainder = total_actions % 9

        if int_part > 0:
            bs_index = int_part - 1
        else:
            bs_index = 0

        if remainder == 0:
            new_action = 6
        else:
            new_action = remainder - 1

        # Recover the BS
        target_bs = self.working_slice.selected_bs[bs_index]

        # Apply the action
        full_flag = self.apply_action(new_action, target_bs)

        info = dict()
        info["satisfaction"] = self.compute_satisfaction()
        new_state = int(info["satisfaction"])

        # Check if the current episode is done
        if new_state >= 75:
            done = True
        else:
            done = False

        reward = 0.0
        if not full_flag:
            # Computing current reward
            if new_state >= 75:
                reward = 100
            elif new_state > self.current_state:
                divisor = 1 if self.current_state == 0 else self.current_state
                reward = 2 * (new_state / divisor)
            elif new_state < self.current_state:
                divisor = 1 if self.current_state == 0 else self.current_state
                new_reward = (new_state/divisor) + 1
                reward = (-2) * new_reward if new_reward > 0 else -100

        return new_state, reward, done, info

    def reset(self):
        self.working_slice = copy.deepcopy(self.network_slice)
        state = int(self.working_slice.cluster.evaluation['satisfaction'])
        return state

    def render(self, mode='human', close=False):
        pass

    def apply_action(self, action, target_bs):
        if target_bs.load == target_bs.max_load:
            full_flag = True
        else:
            full_flag = False
            if action == 0:
                target_bs.increase_bias(6.0)
            elif action == 1:
                target_bs.increase_bias(4.0)
            elif action == 2:
                target_bs.increase_bias(2.0)
            elif action == 3:
                target_bs.increase_bias(1.0)
            elif action == 4:
                target_bs.maintain_bias()
            elif action == 5:
                target_bs.decrease_bias(-1.0)
            elif action == 6:
                target_bs.decrease_bias(-2.0)
            elif action == 7:
                target_bs.decrease_bias(-4.0)
            elif action == 8:
                target_bs.decrease_bias(-6.0)

            target_bs.hetnet.run(first_run_flag=False)
        return full_flag

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
