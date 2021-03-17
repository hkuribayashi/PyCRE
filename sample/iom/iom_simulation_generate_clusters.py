import pickle
import sys

from clustering.PSOAlgorithm import PSOAlgorithm
from clustering.DCM import DCM
from clustering.ClusteringMethod import ClusteringMethod


# Get traffic level
user_density = int(sys.argv[1])

# Get number of BSs
n_bs = int(sys.argv[2])

# Get the min cluster size
min_cluster_size = int(sys.argv[3])

# Get the max cluster size
max_cluster_size = int(sys.argv[4])

# Path
path = sys.argv[5]

# Debug
print("User Density: {} UEs/km2".format(user_density))
print("Number of BSs: {}".format(n_bs))

cluster_list = []

for id_ in range(0, 100):
    print("Current number of clusters found: {}".format(len(cluster_list)))
    print("Loading Hetnet {}:".format(id_))

    # Load hetnet
    filename = '/Users/hugo/Desktop/PyCRE/iom/data/hetnet_{}_{}_{}.obj'.format(user_density, n_bs, id_)
    filehandler = open(filename, 'rb')
    hetnet = pickle.load(filehandler)

    # Instantiate DCM and compute clusters
    dcm = DCM(ClusteringMethod.BIRCH, PSOAlgorithm.DCMPSO, hetnet, user_density)
    dcm.compute_clusters(max_steps=60)

    for target_cluster in dcm.clusters:
        if min_cluster_size < len(target_cluster.ue_list) < max_cluster_size:
            cluster_list.append(target_cluster)

filename = "{}cluster_list_{}_{}.obj".format(path, user_density, n_bs)
file = open(filename, 'wb')

pickle.dump(cluster_list, file)
file.close()
