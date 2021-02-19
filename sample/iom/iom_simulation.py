from clustering.ClusteringMethod import ClusteringMethod
from clustering.DCM import DCM
from clustering.PSOAlgorithm import PSOAlgorithm
from config.network import Network
from mobility.point import Point
from network.bs import BS
from network.hetnet import HetNet

h = HetNet(Network.DEFAULT)

size = 500

p1 = Point(size, size, 10)
bs1 = BS(1, "MBS", p1)

p2 = Point(-size, -size, 10)
bs2 = BS(2, "MBS", p2)

p3 = Point(size, -50, 5)
bs3 = BS(3, "SBS", p3)

p4 = Point(-size, size, 5)
bs4 = BS(4, "SBS", p4)

h.add_bs(bs1)
h.add_bs(bs2)
h.add_bs(bs3)
h.add_bs(bs4)

for step in range(1, Network.DEFAULT.total_time_steps):

    h.run(step)
    print("Step: {} - Global Satisfaction: {} | UEs: {}".format(step, h.evaluation['satisfaction'], len(h.ue_list)))

    if h.evaluation['satisfaction'] <= 50.0:
        print("\n")
        print("Instantiate the Dynamic Clustering Module with DBSCAM algorithm")

        # Instantiate DC Module with DBSCAM algorithm
        dcm = DCM(ClusteringMethod.DBSCAN, PSOAlgorithm.DCMPSO, h)
        dcm.compute_clusters()

        break
