import sys
import pickle

from infrastructure.GWOAlgorithm import GWOAlgorithm
from infrastructure.IOM import IOM

# Get user density
user_density = int(sys.argv[1])

# Get number of BSs
n_bs = int(sys.argv[2])

# Path to save cvs files
path = sys.argv[3]

# Load cluster list object
filename = "/Users/hugo/Desktop/PyCRE/iom/data/cluster_list_{}_{}.obj".format(user_density, n_bs)
filehandler = open(filename, 'rb')
cluster_list = pickle.load(filehandler)

for id_, target_cluster in enumerate(cluster_list):

    # Cluster
    print(target_cluster)

    # Instantiate IO Module with MOGWO Algorithm
    iom = IOM(target_cluster, path=path)

    # Compute the network slice using MOGWO approach
    gwo_slice = iom.compute_network_slice(id_, user_density, GWOAlgorithm.GWO)

    # Save GWO Slice
    filename = "/Users/hugo/Desktop/PyCRE/iom/data/slice_{}_{}_{}.obj".format(user_density, n_bs, id_)
    file = open(filename, 'wb')
    pickle.dump(gwo_slice, file)
    file.close()
