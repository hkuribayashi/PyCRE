import os
import gym
import copy
from stable_baselines3 import DQN as DQN_
from stable_baselines3.common.monitor import Monitor

from algorithms.rl.dqn.RewardCallback import SaveOnBestTrainingRewardCallback


class DQN:
    def __init__(self, id_, network_slice, config, pretrained_model):
        # Set up the ID value
        self.id_ = id_

        # Retrieving configurations
        policy = dict(net_arch=config.net_arch)

        # Check log dir
        self.log_dir = config.log_dir
        os.makedirs(self.log_dir, exist_ok=True)

        self.total_timesteps = config.total_timesteps

        # Set up a monitor for the training phase
        self.callback = SaveOnBestTrainingRewardCallback(self.id_, check_freq=100, log_dir=config.log_dir, verbose=config.verbose)

        # Instantiate the custom gym environment
        self.env = gym.make("gym_pycre:pycre-v0", network_slice=network_slice)

        # Create Monitor
        self.env = Monitor(self.env, config.log_dir)

        # Instantiate the model
        if pretrained_model is None:
            self.model = DQN_("MlpPolicy", self.env, policy_kwargs=policy, learning_rate=config.learning_rate, verbose=config.verbose)
        else:
            self.model = DQN_.load(pretrained_model)

        # Evaluation
        self.evaluation = dict()
        self.evaluation["satisfaction"] = list()
        self.evaluation["load"] = list()
        self.evaluation["satisfaction"].append(network_slice.cluster.evaluation["satisfaction"])

    def learn(self):
        self.model.learn(total_timesteps=self.total_timesteps, callback=self.callback)

    def run(self):
        obs = self.env.reset()
        for _ in range(100):
            action, _states = self.model.predict(obs, deterministic=True)
            obs, reward, done, info = self.env.step(action)
            self.evaluation["satisfaction"].append(info["satisfaction"])
            if done:
                obs = self.env.reset()
