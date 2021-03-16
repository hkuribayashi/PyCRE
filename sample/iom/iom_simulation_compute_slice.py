import pickle

from clustering.ClusteringMethod import ClusteringMethod
from clustering.DCM import DCM
from clustering.PSOAlgorithm import PSOAlgorithm
from infrastructure.GWOAlgorithm import GWOAlgorithm
from infrastructure.IOM import IOM

filename = "/Users/hugo/Desktop/PyCRE/iom/data/cluster_list_300.obj"

filehandler = open(filename, 'rb')
cluster_list = pickle.load(filehandler)

for target_cluster in cluster_list:

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
