import numpy as np

from config.network import Network
from config.qlearning import Agent
from mobility.basic import Point
from network.bs import BS
from network.hetnet import HetNet
from network.ue import UE
from rl.env import Environment
from rl.agent import SingleAgent

# Instantiate a Hetnet using Default Configs
h = HetNet(Network.DEFAULT)

# Deploy a MBS
p0 = Point(0.0, 0.0, 35.0)
mbs = BS(0, 'MBS', p0)

# Deploy a SBS
p1 = Point(50.0, 50.0, 5.0)
sbs = BS(2, 'SBS', p1)

# Add each BS in the Hetnet
h.add_bs(mbs)
h.add_bs(sbs)

# Deploy 10 UEs
for i in range(10):
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
