import sys

from clustering.PSOAlgorithm import PSOAlgorithm
from clustering.DCM import DCM
from clustering.ClusteringMethod import ClusteringMethod
from config.network import Network
from mobility.point import Point
from network.bs import BS
from network.hetnet import HetNet
from utils.misc import save_to_csv


traffic_level = {'10': 100, '60': 600, '100': 999}

# Get traffic level
traffic_key = int(sys.argv[1])

# Get total simulations
simulations = int(sys.argv[2])

# Get total iterations
iterations = int(sys.argv[3])

# Get population size
population_size = int(sys.argv[4])

# Output Directory
path = sys.argv[5]

# Debug
print("Running DCM with DCMPSO: {} simulations, {} iterations and {} particles".format(simulations,
                                                                                       iterations,
                                                                                       population_size))

for key in traffic_level:

    # Debug
    print("Traffic Level: {}%".format(key))

    # Initialize the result variables
    mean_evolution = []
    gbest_evolution = []

    # TODO: Incluir o número de repetições na configuração DEFAULT
    for idx in range(simulations):
        # Current Step
        print("Simulation: {}".format(idx))

        # Instantiate a HetNet
        h = HetNet(Network.DEFAULT)

        # Deploy a MBS
        p0 = Point(0.0, 0.0, 35.0)
        mbs = BS(0, 'MBS', p0)

        # Add each BS in the HetNet
        h.add_bs(mbs)

        # Run the HetNet
        h.run(traffic_level[key])

        # Instantiate DC Module with DBSCAM algorithm
        dcm = DCM(ClusteringMethod.DBSCAN, PSOAlgorithm.DCMPSO, h, traffic_level[key])

        # Run DCM
        results = dcm.get_cluster_analysis(population_size, iterations)

        # Save Results
        save_to_csv(results, path, "dcm_cluster_statistics_{}.csv".format(key))

    print("\n")
