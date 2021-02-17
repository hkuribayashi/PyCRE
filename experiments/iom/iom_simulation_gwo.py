import numpy as np

from config.network import Network
from mobility.point import Point
from network.bs import BS
from network.hetnet import HetNet
from si.gwo.GWO import GWO

# Instantiate a HetNet
h = HetNet(Network.DEFAULT)

# Deploy a MBS
p0 = Point(0.0, 0.0, 35.0)
mbs = BS(0, 'MBS', p0)

# Add each BS in the HetNet
h.add_bs(mbs)

# Run the HetNet with 10% of UEs
h.run(100)

# Extract UE position to a numpy array
data = []
for ue in h.ue_list:
    data.append([ue.point.x, ue.point.y])
data = np.array(data)

# Instantiate the GWO algorithm
g = GWO(data, 150, 200)

g.search()