import numpy as np


min_exploration_rate = 0.01
max_exploration_rate = 1
exploration_decay_rate = 0.01

for episode in range(1000):
    exploration_rate = min_exploration_rate + (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * episode)
    print(exploration_rate)
