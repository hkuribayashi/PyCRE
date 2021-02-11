import numpy as np
import random


class SingleAgent:
    def __init__(self, env, config):
        self.env = env
        self.config = config

        # Action Space
        self.action_space_size = env.action_space.n

        # Observation Space
        self.state_space_size = env.observation_space.n

        # Q-table: State Space x Action Space
        self.q_table = np.zeros((self.state_space_size, self.action_space_size))

        self.num_episodes = config.num_episodes
        self.max_steps_per_episode = config.max_steps_per_episode
        self.learning_rate = config.learning_rate
        self.discount_rate = config.discount_rate
        self.max_exploration_rate = config.max_exploration_rate
        self.min_exploration_rate = config.min_exploration_rate
        self.exploration_decay_rate = config.exploration_decay_rate

        self.max_iter_per_state = config.max_iter_per_state

        self.satisfaction_all_episodes = []

    def run(self):

        flag = False
        exploration_rate = self.max_exploration_rate

        # Q-learning algorithm
        for episode in range(self.num_episodes):

            # initialize new episode params
            state = self.env.reset()
            satisfaction_current_episode = 0
            steps_per_episode = 0
            iter_per_state = 0

            for step in range(self.max_steps_per_episode):

                # Exploration-exploitation trade-off
                exploration_rate_threshold = random.uniform(0, self.max_exploration_rate)
                if (exploration_rate_threshold > exploration_rate) or flag:
                    action = np.argmax(self.q_table[state, :])
                    flag = False
                else:
                    action = self.env.action_space.sample()

                # Take new action
                new_state, reward, done, changed, info = self.env.step(action, state)

                # Update Q-table
                self.q_table[state, action] = self.q_table[state, action] * (1 - self.learning_rate) + \
                                         self.learning_rate * (reward + self.discount_rate * np.max(self.q_table[new_state, :]))

                if changed:
                    iter_per_state = 0
                else:
                    iter_per_state = iter_per_state + 1

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
            exploration_rate = self.min_exploration_rate + (self.max_exploration_rate - self.min_exploration_rate) * np.exp(-self.exploration_decay_rate * episode)

            # Add current episode reward to total rewards list
            if steps_per_episode == 0:
                steps_per_episode = 1
            self.satisfaction_all_episodes.append(satisfaction_current_episode / steps_per_episode)

            # Check verbose mode
            if self.config.verbose:
                # Print Q-Table
                if episode % 100 == 0:
                    print('Q_Table Episode: {}'.format(episode))
                    print(self.q_table)
                    print('Current State: {}'.format(state))
                    print()
                    self.env.hetnet.debug()

    def get_metrics(self):
        return self.satisfaction_all_episodes
