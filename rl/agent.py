import numpy as np
import random


class Agent:
    def __init__(self, env):
        self.env = env

        # Action Space
        self.action_space_size = env.action_space.n

        # Observation Space
        self.state_space_size = env.observation_space.n

        # Q-table: State Space x Action Space
        self.q_table = np.zeros((self.state_space_size, self.action_space_size))

        self.num_episodes = 10000
        self.max_steps_per_episode = 1000

        self.learning_rate = 0.1
        self.discount_rate = 0.99

        self.exploration_rate = 1
        self.max_exploration_rate = 1
        self.min_exploration_rate = 0.01
        self.exploration_decay_rate = 0.001

        self.max_iter_per_state = self.max_steps_per_episode * 0.2
        self.satisfaction_all_episodes = []

    def run(self):

        flag = False

        # Q-learning algorithm
        for episode in range(self.num_episodes):

            # initialize new episode params
            state = self.env.reset()
            satisfaction_current_episode = 0
            steps_per_episode = 0
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

                # Add new satisfaction
                satisfaction_current_episode += info['satisfaction']

                if self.max_iter_per_state <= iter_per_state:
                    flag = True

                # Break
                if done or flag:
                    break

                steps_per_episode = steps_per_episode + 1

            # Exploration rate decay
            self.exploration_rate = self.min_exploration_rate + \
                               (self.max_exploration_rate - self.min_exploration_rate) * np.exp(-self.exploration_decay_rate * episode)

            # Add current episode reward to total rewards list
            self.satisfaction_all_episodes.append(satisfaction_current_episode/steps_per_episode)

            # Print Q-Table
            if episode % 1000 == 0:
                print('Q_Table Episode: {}'.format(episode))
                print(self.q_table)
                print('Current State: {}'.format(state))
                print()

    def get_statistics(self):
        # Separa 10000 episódios em vários arrays de 1000 em 1000
        satisfaction_per_thosand_episodes = np.split(np.array(self.satisfaction_all_episodes), self.num_episodes / 1000)

        count = 1000
        print("********Average satisfaction per thousand episodes********\n")
        for s in satisfaction_per_thosand_episodes:
            avg_satisfaction = sum(s / 1000)
            print(count, ": ", str(avg_satisfaction))
            count += 1000

            # Print updated Q-table
        print("\n\n********Q-table********\n")
        print(self.q_table)
