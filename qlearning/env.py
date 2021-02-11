from qlearning.action import ActionSpace
from qlearning.observation import ObservationSpace


class Environment:

    def __init__(self, hetnet):
        self.action_space = ActionSpace(7)
        self.observation_space = ObservationSpace(101)
        self.hetnet = hetnet
        self.hetnet.optimizationEngine()
        print(self.hetnet.evaluation)
        self.hetnet.debug()

    def reset(self):
        self.hetnet.reset_hetnet()
        self.hetnet.optimizationEngine()
        state = int(self.hetnet.evaluation['satisfaction'])
        return state

    def step(self, action, state):

        # TODO: Filter per SBS
        bs_0 = self.hetnet.list_bs[1]

        if action == 0:
            bs_0.increase_bias(20.0)
        elif action == 1:
            bs_0.increase_bias(10.0)
        elif action == 2:
            bs_0.increase_bias(5.0)
        elif action == 3:
            bs_0.maintain_bias()
        elif action == 4:
            bs_0.decrease_bias(-5.0)
        elif action == 5:
            bs_0.decrease_bias(-10.0)
        elif action == 6:
            bs_0.decrease_bias(-20.0)

        self.hetnet.optimizationEngine()

        new_state = int(self.hetnet.evaluation['satisfaction'])
        if new_state >= 95:
            reward = 100.0
            has_done = True
            has_changed = True
        elif new_state > state:
            reward = 0.01
            has_done = False
            has_changed = True
        elif new_state < state:
            reward = -0.01
            has_done = False
            has_changed = True
        else:
            reward = 0.0
            has_done = False
            has_changed = False

        info = self.hetnet.evaluation

        return new_state, reward, has_done, has_changed, info
