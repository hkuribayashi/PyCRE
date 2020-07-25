import numpy as np

from config.env import Configuration
from mobility.basic import Point
from network.bs import BS
from network.hetnet import HetNet
from network.ue import UE

# Instantiate a Hetnet using Default Configs
h = HetNet(Configuration.DEFAULT)

# Deploy a MBS
p1 = Point(0.0, 0.0, 35.0)
mbs = BS(1, 'MBS', p1)

# Deploy a SBS
p2 = Point(50.0, 50.0, 5.0)
sbs_1 = BS(2, 'SBS', p2)

# Deploy another SBS
p3 = Point(-50.0, -50.0, 5.0)
sbs_2 = BS(3, 'SBS', p3)

# Deploy another SBS
p4 = Point(-50.0, 50.0, 5.0)
sbs_3 = BS(3, 'SBS', p4)

# Deploy another SBS
p5 = Point(50.0, -50.0, 5.0)
sbs_4 = BS(3, 'SBS', p5)

# Add each BS in the Hetnet
h.add_bs(mbs)
h.add_bs(sbs_1)
h.add_bs(sbs_2)
h.add_bs(sbs_3)
h.add_bs(sbs_4)

# Deploy 20 UEs
for i in range(20):
    x = np.random.randint(-100, 100)
    y = np.random.randint(-100, 100)
    p_i = Point(x, y, 5.0)
    ue = UE(i, p_i)
    h.add_ue(ue)

# Run de Hetnet
h.run()

# Print de Evaluation Metrics
print('Evaluation: {}'.format(h.evaluation))

# Agents's Actions
sbs_1.increase_bias()
sbs_2.decrease_bias()
sbs_3.maintain_bias()
sbs_4.increase_bias()

# Re-Run de Hetnet
h.run()

# Print de Evaluation Metrics
print('Evaluation: {}'.format(h.evaluation))