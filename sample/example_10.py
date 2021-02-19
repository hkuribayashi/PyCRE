from config.network import Network
from mobility.point import Point
from network.bs import BS
from network.hetnet import HetNet

h = HetNet(Network.DEFAULT)

p1 = Point(50, 50, 10)
bs1 = BS(1, "MBS", p1)

p3 = Point(50, -50, 5)
bs3 = BS(3, "SBS", p3)

p4 = Point(-50, 50, 5)
bs4 = BS(4, "SBS", p4)

h.add_bs(bs1)
h.add_bs(bs3)
h.add_bs(bs4)

h.run(31)
print("Evaluation: {} | UEs: {}".format(h.evaluation['satisfaction'], len(h.ue_list)))
