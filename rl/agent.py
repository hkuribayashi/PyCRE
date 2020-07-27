import numpy as np
import gym
import random
import time
from IPython.display import clear_output


class Agent:
    def __init__(self, env):
        # self.env = gym.make("FrozenLake-v0")
        self.env = env

        # Espaço de Acoes: 3 (aumentar, diminuir ou manter)
        self.action_space_size = env.action_space.n

        # Espaco de Estados: 10
        self.state_space_size = env.observation_space.n

        self.q_table = np.zeros((self.state_space_size, self.action_space_size))

        self.num_episodes = 1000
        self.max_steps_per_episode = 1000

        self.learning_rate = 0.1
        self.discount_rate = 0.99

        self.exploration_rate = 1
        self.max_exploration_rate = 1
        self.min_exploration_rate = 0.01
        self.exploration_decay_rate = 0.001

        self.rewards_all_episodes = []
        self.ues_atendidos_all_episodes = []

    def run(self):
        # Q-learning algorithm
        for episode in range(self.num_episodes):
            # initialize new episode params
            state = self.env.reset()
            done = False
            rewards_current_episode = 0

            for step in range(self.max_steps_per_episode):

                # Exploration-exploitation trade-off
                exploration_rate_threshold = random.uniform(0, 1)
                if exploration_rate_threshold > self.exploration_rate:
                    action = np.argmax(self.q_table[state, :])
                else:
                    action = self.env.action_space.sample()

                # Take new action
                new_state, reward, done, info = self.env.step(action)

                # Update Q-table
                self.q_table[state, action] = self.q_table[state, action] * (1 - self.learning_rate) + \
                                         self.learning_rate * (reward + self.discount_rate * np.max(self.q_table[new_state, :]))

                # Set new state
                state = new_state

                # Add new reward
                rewards_current_episode += reward

            if episode % 100 == 0:
                print('Q_Table Episode: {}'.format(episode))
                print(self.q_table)
                print('Current State: {}'.format(state))
                print()

            # Break
            if done:
                print('Finish')
                break

            # Exploration rate decay
            self.exploration_rate = self.min_exploration_rate + \
                               (self.max_exploration_rate - self.min_exploration_rate) * np.exp(-self.exploration_decay_rate * episode)

            # Add current episode reward to total rewards list
            self.rewards_all_episodes.append(rewards_current_episode)

    def get_metrics(self):

        # Calculate and print the average reward per ten episodes
        rewards_per_thousand_episodes = np.split(np.array(self.rewards_all_episodes),self.num_episodes/10)
        ues_per_thousand_episodes = np.split(np.array(self.ues_atendidos_all_episodes), self.num_episodes / 10)
        count = 10

        print("********Average reward per thousand episodes********\n")
        for r in ues_per_thousand_episodes:
            print(count, ": ", str(sum(r/1000)))
            count += 10
        print('Debug')
        print(self.q_table)
