import numpy as np

from config.network import Network
from config.qlearning import Agent
from mobility.point import Point
from network.bs import BS
from network.hetnet import HetNet
from network.ue import UE
from qlearning.env import Environment
from qlearning.agent import SingleAgent

# Instantiate a Hetnet using Default Configs
h = HetNet(Network.DEFAULT)



# Deploy 10 UEs
for i in range(20):
    x = np.random.randint(30, 80)
    y = np.random.randint(30, 80)
    p_i = Point(x, y, 5.0)
    ue = UE(i, p_i)
    h.add_ue(ue)

# Deploy 22 UEs
for i in range(10, 32):
    x = np.random.randint(-100, 100)
    y = np.random.randint(-100, 100)
    p_i = Point(x, y, 5.0)
    ue = UE(i, p_i)
    h.add_ue(ue)

env = Environment(h)
a = SingleAgent(env, Agent.DEFAULT)
a.run()
a.get_metrics()
