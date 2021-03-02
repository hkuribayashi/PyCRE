import random
import numpy as np

from clustering.ClusteringMethod import ClusteringMethod
from clustering.DCM import DCM
from clustering.PSOAlgorithm import PSOAlgorithm
from config.network import Network
from infrastructure.GWOAlgorithm import GWOAlgorithm
from infrastructure.IOM import IOM
from mobility.point import Point
from network.bs import BS
from network.hetnet import HetNet

h = HetNet(Network.DEFAULT)

# Generating MBSs
size = 700
p1 = Point(size, size, Network.DEFAULT.mbs_height)
bs1 = BS(1, "MBS", p1)

p2 = Point(-size, -size, Network.DEFAULT.mbs_height)
bs2 = BS(2, "MBS", p2)

p3 = Point(size, -size, Network.DEFAULT.mbs_height)
bs3 = BS(3, "MBS", p3)

p4 = Point(-size, size, Network.DEFAULT.mbs_height)
bs4 = BS(4, "MBS", p4)

h.add_bs(bs1)
h.add_bs(bs2)
h.add_bs(bs3)
h.add_bs(bs4)

side = np.sqrt(Network.DEFAULT.simulation_area)

# Generating SBSs
for id_ in range(5, 45):
    x = random.uniform(-side, side)
    y = random.uniform(-side, side)
    p_x = Point(x, y, Network.DEFAULT.sbs_height)
    bs_x = BS(id_, "SBS", p_x)
    h.add_bs(bs_x)

for step in range(13, Network.DEFAULT.total_time_steps):

    h.run(step)
    print("Step: {} - Global Satisfaction: {} | UEs: {}".format(step, h.evaluation['satisfaction'], len(h.ue_list)))

    if h.evaluation['satisfaction'] <= (Network.DEFAULT.outage_threshold * 100):

        # Plot the hetnet visual representation
        h.debug()

        print("\n")
        print("Instantiate the Dynamic Clustering Module with DBSCAM algorithm")

        # Instantiate DC Module with DBSCAM algorithm
        dcm = DCM(ClusteringMethod.DBSCAN, PSOAlgorithm.DCMPSO, h, step)
        dcm.compute_clusters()

        for target_cluster in dcm.clusters:
            print(target_cluster)
            # Instantiate IO Module with MOGWO Algorithm
            iom = IOM(target_cluster, GWOAlgorithm.GWO)

            # Compute the network slice
            # network_slice = iom.compute_network_slice()

            # Bound the generated network slice the with inputted cluster
            # target_cluster.network_slice = network_slice

        break
