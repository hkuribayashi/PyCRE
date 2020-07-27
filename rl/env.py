from rl.action import ActionSpace
from rl.observation import ObservationSpace


class Environment:

    def __init__(self, hetnet):
        self.action_space = ActionSpace(2)
        self.observation_space = ObservationSpace(10)
        self.hetnet = hetnet
        self.hetnet.run()
        self.hetnet.debug()

    def reset(self):

        if int(self.hetnet.evaluation['satisfaction']) >= 90:
            state = 9
        elif int(self.hetnet.evaluation['satisfaction']) >= 80:
            state = 8
        elif int(self.hetnet.evaluation['satisfaction']) >= 70:
            state = 7
        elif int(self.hetnet.evaluation['satisfaction']) >= 60:
            state = 6
        elif int(self.hetnet.evaluation['satisfaction']) >= 50:
            state = 5
        elif int(self.hetnet.evaluation['satisfaction']) >= 40:
            state = 4
        elif int(self.hetnet.evaluation['satisfaction']) >= 30:
            state = 3
        elif int(self.hetnet.evaluation['satisfaction']) >= 20:
            state = 2
        elif int(self.hetnet.evaluation['satisfaction']) >= 10:
            state = 1
        else:
            state = 0

        return state

    def step(self, action):

        bs_0 = self.hetnet.list_bs[1]

        if action == 0:
            bs_0.increase_bias()
        else:
            bs_0.decrease_bias()

        self.hetnet.run()

        if int(self.hetnet.evaluation['satisfaction']) >= 90:
            new_state = 9
            reward = 5.0
        elif int(self.hetnet.evaluation['satisfaction']) >= 80:
            new_state = 8
            reward = 4.0
        elif int(self.hetnet.evaluation['satisfaction']) >= 70:
            new_state = 7
            reward = 3.0
        elif int(self.hetnet.evaluation['satisfaction']) >= 60:
            new_state = 6
            reward = 2.0
        elif int(self.hetnet.evaluation['satisfaction']) >= 50:
            new_state = 5
            reward = 1.0
        elif int(self.hetnet.evaluation['satisfaction']) >= 40:
            new_state = 4
            reward = 0.5
        elif int(self.hetnet.evaluation['satisfaction']) >= 30:
            new_state = 3
            reward = 0.25
        elif int(self.hetnet.evaluation['satisfaction']) >= 20:
            new_state = 2
            reward = 0.125
        elif int(self.hetnet.evaluation['satisfaction']) >= 10:
            new_state = 1
            reward = 0.0625
        else:
            new_state = 0
            reward = 0.03125

        if self.hetnet.evaluation['satisfaction'] >= 90:
            done = True
        else:
            done = False

        info = self.hetnet.evaluation

        return new_state, reward, done, info
