from rl.action import ActionSpace
from rl.observation import ObservationSpace


class Environment:

    def __init__(self, hetnet):
        self.action_space = ActionSpace(7)
        self.observation_space = ObservationSpace(101)
        self.hetnet = hetnet
        self.hetnet.run()
        print(self.hetnet.evaluation)

    def reset(self):
        self.hetnet.reset_hetnet()
        self.hetnet.run()
        state = int(self.hetnet.evaluation['satisfaction'])
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
            bs_0.decrease_bias(-20.0)

        self.hetnet.run()

        new_state = int(self.hetnet.evaluation['satisfaction'])
        if new_state >= 90:
            reward = 100.0
            done = True
        elif new_state > state:
            reward = 0.01
            done = False
        elif new_state < state:
            reward = -0.01
            done = False
        else:
            reward = 0.0
            done = False

        #print('Episode: {}'.format(episode))
        #print('Step: {}'.format(step))
        #print('Last Action: {}'.format(action))
        #print('Old State: {}'.format(state))
        #print('New State: {}'.format(new_state))
        #self.hetnet.debug()
        #print()

        info = self.hetnet.evaluation

        return new_state, reward, done, info
