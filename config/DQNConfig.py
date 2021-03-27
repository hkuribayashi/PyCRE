from enum import Enum


class DQNConfig(Enum):

    DEFAULT = (10000, 0.99, 0.1, [32, 32], "/Users/hugo/Desktop/PyCRE/rlm/logs/", 0)

    def __init__(self, total_timesteps, gamma, learning_rate, net_arch, log_dir, verbose):

        self.total_timesteps = total_timesteps
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.net_arch = net_arch
        self.log_dir = log_dir
        self.verbose = verbose
