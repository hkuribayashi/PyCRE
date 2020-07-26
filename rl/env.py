from rl.action import ActionSpace
from rl.observation import ObservationSpace


class Environment:

    def __init__(self, hetnet):
        self.action_space = ActionSpace(8)
        self.observation_space = ObservationSpace(100)
        self.hetnet = hetnet
        self.hetnet.run()

    def reset(self):
        return 0

    def step(self, action, episode, step):

        bs_0 = self.hetnet.list_bs[0]
        bs_1 = self.hetnet.list_bs[1]
        bs_2 = self.hetnet.list_bs[2]
        bs_3 = self.hetnet.list_bs[3]

        if action == 0:
            bs_0.increase_bias()
        elif action == 1:
            bs_0.decrease_bias()
        elif action == 2:
            bs_1.increase_bias()
        elif action == 3:
            bs_1.decrease_bias()
        elif action == 4:
            bs_2.increase_bias()
        elif action == 5:
            bs_2.decrease_bias()
        elif action == 6:
            bs_3.increase_bias()
        else:
            bs_3.decrease_bias()


        self.hetnet.run()

        new_state = int(self.hetnet.evaluation['satisfaction'])

        if new_state >= 80:
            reward = 1.0
        else:
            reward = 0.0

        if self.hetnet.evaluation['satisfaction'] == 100:
            done = True
        else:
            done = False

        info = self.hetnet.evaluation

        if episode == 99 and step == 999:
            self.hetnet.debug()

        return new_state, reward, done, info
