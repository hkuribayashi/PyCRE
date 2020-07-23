import numpy as np

from config.env import Configuration
from mobility.basic import Point
from network.bs import BS
from network.hetnet import HetNet
from network.ue import UE

# Cria uma Hetnet
h = HetNet(Configuration.DEFAULT)

# Cria uma MBS
p1 = Point(0.0, 0.0, 35.0)
mbs = BS(1, 'MBS', p1)

# Cria uma SBS
p2 = Point(100.0, 0.0, 5.0)
sbs_1 = BS(2, 'SBS', p2)

# Cria outra SBS
p3 = Point(-100.0, 0.0, 5.0)
sbs_2 = BS(3, 'SBS', p3)

# Registra as BSs na Hetnet
h.add_bs(mbs)
h.add_bs(sbs_1)
h.add_bs(sbs_2)

# Cria 10 UEs
for i in range(20):
    x = np.random.randint(-100, 100)
    y = np.random.randint(-100, 100)
    p_i = Point(x, y, 5.0)
    ue = UE(i, p_i)
    h.add_ue(ue)

h.run()
