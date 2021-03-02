import pickle

from clustering.ClusteringMethod import ClusteringMethod
from clustering.DCM import DCM
from clustering.PSOAlgorithm import PSOAlgorithm
from infrastructure.GWOAlgorithm import GWOAlgorithm
from infrastructure.IOM import IOM

hetnet_filename = "/Users/hugo/Desktop/PyCRE/data2/hetnet.obj"

filehandler = open(hetnet_filename, 'rb')
hetnet = pickle.load(filehandler)

dcm = DCM(ClusteringMethod.DBSCAN, PSOAlgorithm.DCMPSO, hetnet, 10, 6, 398)
dcm.compute_clusters()

for target_cluster in dcm.clusters:

    # Cluster
    print(target_cluster)

    # Instantiate IO Module with MOGWO Algorithm
    iom = IOM(target_cluster, path="/Users/hugo/Desktop/PyCRE/iom/csv/")

    # Compute the network slice
    iom.compute_network_slice(GWOAlgorithm.MOGWO)

    # Instantiate IO Module with GWO Algorithm
    # iom = IOM(target_cluster, GWOAlgorithm.GWO)

    # Compute the network slice
    # iom.compute_network_slice(path="/Users/hugo/Desktop/PyCRE/iom/csv/")

    # Start the RLM for each network slice
    # print(target_cluster.networkslice)
