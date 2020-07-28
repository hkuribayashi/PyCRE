from rl.action import ActionSpace
from rl.observation import ObservationSpace


class Environment:

    def __init__(self, hetnet):
        self.action_space = ActionSpace(7)
        self.observation_space = ObservationSpace(20)
        self.hetnet = hetnet
        self.hetnet.run()
        print(self.hetnet.evaluation)

    def reset(self):

        if int(self.hetnet.evaluation['satisfaction']) >= 95:
            state = 19
        elif int(self.hetnet.evaluation['satisfaction']) >= 90:
            state = 18
        elif int(self.hetnet.evaluation['satisfaction']) >= 85:
            state = 17
        elif int(self.hetnet.evaluation['satisfaction']) >= 80:
            state = 16
        elif int(self.hetnet.evaluation['satisfaction']) >= 75:
            state = 15
        elif int(self.hetnet.evaluation['satisfaction']) >= 70:
            state = 14
        elif int(self.hetnet.evaluation['satisfaction']) >= 65:
            state = 13
        elif int(self.hetnet.evaluation['satisfaction']) >= 60:
            state = 12
        elif int(self.hetnet.evaluation['satisfaction']) >= 55:
            state = 11
        elif int(self.hetnet.evaluation['satisfaction']) >= 50:
            state = 10
        elif int(self.hetnet.evaluation['satisfaction']) >= 45:
            state = 9
        elif int(self.hetnet.evaluation['satisfaction']) >= 40:
            state = 8
        elif int(self.hetnet.evaluation['satisfaction']) >= 35:
            state = 7
        elif int(self.hetnet.evaluation['satisfaction']) >= 30:
            state = 6
        elif int(self.hetnet.evaluation['satisfaction']) >= 25:
            state = 5
        elif int(self.hetnet.evaluation['satisfaction']) >= 20:
            state = 4
        elif int(self.hetnet.evaluation['satisfaction']) >= 15:
            state = 3
        elif int(self.hetnet.evaluation['satisfaction']) >= 10:
            state = 2
        elif int(self.hetnet.evaluation['satisfaction']) >= 5:
            state = 1
        else:
            state = 0

        return state

    def step(self, action, episode, state, step):

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
            bs_0.decrease_bias(-15.0)

        self.hetnet.run()

        if int(self.hetnet.evaluation['satisfaction']) >= 95:
            new_state = 19
            reward = 2.0
        elif int(self.hetnet.evaluation['satisfaction']) >= 90:
            new_state = 18
            reward = 0.98526125
        elif int(self.hetnet.evaluation['satisfaction']) >= 85:
            new_state = 17
            reward = 0.65684084
        elif int(self.hetnet.evaluation['satisfaction']) >= 80:
            new_state = 16
            reward = 0.43789389
        elif int(self.hetnet.evaluation['satisfaction']) >= 75:
            new_state = 15
            reward = 0.29192926
        elif int(self.hetnet.evaluation['satisfaction']) >= 70:
            new_state = 14
            reward = 0.19461951
        elif int(self.hetnet.evaluation['satisfaction']) >= 65:
            new_state = 13
            reward = 0.12974634
        elif int(self.hetnet.evaluation['satisfaction']) >= 60:
            new_state = 12
            reward = 0.08649756
        elif int(self.hetnet.evaluation['satisfaction']) >= 55:
            new_state = 11
            reward = 0.05766504
        elif int(self.hetnet.evaluation['satisfaction']) >= 50:
            new_state = 10
            reward = 0.03844336
        elif int(self.hetnet.evaluation['satisfaction']) >= 45:
            new_state = 9
            reward = 0.02562891
        elif int(self.hetnet.evaluation['satisfaction']) >= 40:
            new_state = 8
            reward = 0.01708594
        elif int(self.hetnet.evaluation['satisfaction']) >= 35:
            new_state = 7
            reward = 0.01139062
        elif int(self.hetnet.evaluation['satisfaction']) >= 30:
            new_state = 6
            reward = 0.00789375
        elif int(self.hetnet.evaluation['satisfaction']) >= 25:
            new_state = 5
            reward = 0.0050625
        elif int(self.hetnet.evaluation['satisfaction']) >= 20:
            new_state = 4
            reward = 0.003375
        elif int(self.hetnet.evaluation['satisfaction']) >= 15:
            new_state = 3
            reward = 0.00225
        elif int(self.hetnet.evaluation['satisfaction']) >= 10:
            new_state = 2
            reward = 0.0015
        elif int(self.hetnet.evaluation['satisfaction']) >= 5:
            new_state = 1
            reward = 0.001
        else:
            new_state = 0
            reward = 0.00001

        #print('Episode: {}'.format(episode))
        #print('Step: {}'.format(step))
        #print('Last Action: {}'.format(action))
        #print('Old State: {}'.format(state))
        #print('New State: {}'.format(new_state))
        #self.hetnet.debug()
        #print()

        if self.hetnet.evaluation['satisfaction'] >= 95:
            done = True
        else:
            done = False

        info = self.hetnet.evaluation

        return new_state, reward, done, info
