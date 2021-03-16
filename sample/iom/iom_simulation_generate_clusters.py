import pickle
import sys

from clustering.PSOAlgorithm import PSOAlgorithm
from clustering.DCM import DCM
from clustering.ClusteringMethod import ClusteringMethod
from config.network import Network
from network.hetnet import HetNet


# Get traffic level
user_density = int(sys.argv[1])

# Get total number of clusters to find
n_clusters = int(sys.argv[2])

# Get the min cluster size
min_cluster_size = int(sys.argv[3])

# Get the max cluster size
max_cluster_size = int(sys.argv[4])

# Path
path = sys.argv[5]

# Debug
print("Running DCM with DCMPSO")

# Debug
print("User Density: {} UEs/km2".format(user_density))

counter = 0
cluster_list = []

while counter < n_clusters:
    print("Current number of clusters found: {}".format(counter))

    # Instantiate a HetNet
    h = HetNet(Network.DEFAULT)
    h.populate_bs()

    # Run the HetNet
    h.run(user_density)

    # Instantiate DCM and compute clusters
    dcm = DCM(ClusteringMethod.BIRCH, PSOAlgorithm.DCMPSO, h, user_density)
    dcm.compute_clusters(max_steps=60)

    for target_cluster in dcm.clusters:
        if min_cluster_size < len(target_cluster.ue_list) < max_cluster_size:
            cluster_list.append(target_cluster)
            counter += 1

filename = "{}cluster_list_{}.obj".format(path, user_density)
file = open(filename, 'wb')

pickle.dump(cluster_list, file)
file.close()
