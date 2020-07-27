import numpy as np

from config.env import Configuration
from mobility.basic import Point
from network.bs import BS
from network.hetnet import HetNet
from network.ue import UE

h = HetNet(Configuration.DEFAULT)

# Deploy a MBS
p1 = Point(0.0, 0.0, 35.0)
mbs = BS(1, 'MBS', p1)

# Deploy a SBS
p2 = Point(50.0, 50.0, 5.0)
sbs_1 = BS(2, 'SBS', p2)


# Add each BS in the Hetnet
h.add_bs(mbs)
h.add_bs(sbs_1)

# Deploy 20 UEs
for i in range(5):
    x = np.random.randint(-60, 60)
    y = np.random.randint(-60, 60)
    p_i = Point(x, y, 5.0)
    ue = UE(i, p_i)
    h.add_ue(ue)

h.run()

sbs_1.decrease_bias()
h.run()

sbs_1.decrease_bias()
h.run()

sbs_1.decrease_bias()
h.run()

sbs_1.increase_bias()
h.run()

sbs_1.increase_bias()
h.run()

sbs_1.increase_bias()
h.run()

sbs_1.increase_bias()
h.run()

sbs_1.increase_bias()
h.run()
