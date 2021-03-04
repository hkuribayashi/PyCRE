import pickle

from clustering.ClusteringMethod import ClusteringMethod
from clustering.DCM import DCM
from clustering.PSOAlgorithm import PSOAlgorithm
from config.network import Network
from infrastructure.GWOAlgorithm import GWOAlgorithm
from infrastructure.IOM import IOM

# Instantiate a HetNet
from mobility.point import Point
from network.bs import BS
from network.hetnet import HetNet

h = HetNet(Network.DEFAULT)

# Deploy a MBS
p0 = Point(0.0, 0.0, 35.0)
mbs = BS(0, 'MBS', p0)

# Add each BS in the HetNet
h.add_bs(mbs)

# Run the HetNet
h.run(300)

dcm = DCM(ClusteringMethod.DBSCAN, PSOAlgorithm.DCMPSO, h, 300)
dcm.compute_clusters(population_size=300)

for target_cluster in dcm.clusters:

    # Cluster
    print(target_cluster)

    # Instantiate IO Module with MOGWO Algorithm
    # iom = IOM(target_cluster, path="/Users/hugo/Desktop/PyCRE/iom/csv/")

    # Compute the network slice
    # iom.compute_network_slice(GWOAlgorithm.MOGWO)

    # Instantiate IO Module with GWO Algorithm
    # iom = IOM(target_cluster, GWOAlgorithm.GWO)

    # Compute the network slice
    # iom.compute_network_slice(GWOAlgorithm.MOGWO)

    # Start the RLM for each network slice
    # print(target_cluster.networkslice)
