import numpy as np
import gym
import random
import time
from IPython.display import clear_output


class Agent:
    def __init__(self, env):
        # self.env = gym.make("FrozenLake-v0")
        self.env = env

        # Espaço de Acoes: 7 (aumentar ou diminuir)
        self.action_space_size = env.action_space.n

        # Espaco de Estados: 20
        self.state_space_size = env.observation_space.n

        self.q_table = np.zeros((self.state_space_size, self.action_space_size))

        self.num_episodes = 10000
        self.max_steps_per_episode = 1000

        self.learning_rate = 0.1
        self.discount_rate = 0.99

        self.exploration_rate = 1
        self.max_exploration_rate = 1
        self.min_exploration_rate = 0.01
        self.exploration_decay_rate = 0.001

        self.max_iter_per_state = self.max_steps_per_episode * 0.5

        self.rewards_all_episodes = []

    def run(self):

        flag = False

        # Q-learning algorithm
        for episode in range(self.num_episodes):

            # initialize new episode params
            state = self.env.reset()
            done = False
            rewards_current_episode = 0
            iter_per_state = 0

            for step in range(self.max_steps_per_episode):

                # Exploration-exploitation trade-off
                exploration_rate_threshold = random.uniform(0, 1)
                if exploration_rate_threshold > self.exploration_rate or flag:
                    action = np.argmax(self.q_table[state, :])
                    flag = False
                else:
                    action = self.env.action_space.sample()

                # Take new action
                new_state, reward, done, info = self.env.step(action, episode, state, step)

                # Update Q-table
                self.q_table[state, action] = self.q_table[state, action] * (1 - self.learning_rate) + \
                                         self.learning_rate * (reward + self.discount_rate * np.max(self.q_table[new_state, :]))

                if new_state == state:
                    iter_per_state = iter_per_state + 1
                else:
                    iter_per_state = 0

                # Set new state
                state = new_state

                # Add new reward
                rewards_current_episode += reward

                if self.max_iter_per_state <= iter_per_state:
                    flag = True

                # Break
                if done or flag:
                    #print('Finish at Episode: {}'.format(episode))
                    # print()
                    break

            # Exploration rate decay
            self.exploration_rate = self.min_exploration_rate + \
                               (self.max_exploration_rate - self.min_exploration_rate) * np.exp(-self.exploration_decay_rate * episode)

            # Add current episode reward to total rewards list
            self.rewards_all_episodes.append(rewards_current_episode)

            # Print Q-Table
            if episode % 1000 == 0:
                print('Q_Table Episode: {}'.format(episode))
                print(self.q_table)
                print('Current State: {}'.format(state))
                print()

    def get_statistics(self):
        # Calculate and print the average reward per thousand episodes
        rewards_per_thosand_episodes = np.split(np.array(self.rewards_all_episodes), self.num_episodes / 1000)
        count = 1000
        print("********Average reward per thousand episodes********\n")
        for r in rewards_per_thosand_episodes:
            avg_reward = sum(r / 1000)
            print(count, ": ", str(avg_reward))
            count += 1000

            # Print updated Q-table
        print("\n\n********Q-table********\n")
        print(self.q_table)