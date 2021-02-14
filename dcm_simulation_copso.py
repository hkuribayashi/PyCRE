from clustering.PSOAlgorithm import PSOAlgorithm
from clustering.DCM import DCM
from clustering.ClusteringMethod import ClusteringMethod
from mobility.point import Point
from network.bs import BS
from network.hetnet import HetNet
from utils.misc import save_to_csv
from config.network import Network


traffic_level = {'100': 999}

for key in traffic_level:

    # Start the Dynamic Clustering Module variables
    mean_evolution_list_100_pop_200 = []
    mean_evolution_list_100_pop_200_gbest = []

    # TODO: Incluir o número de repetições na configuração DEFAULT
    for idx in range(50):
        print("Step: {}".format(idx))

        # Instantiate a HetNet
        h = HetNet(Network.DEFAULT)

        # Deploy a MBS
        p0 = Point(0.0, 0.0, 35.0)
        mbs = BS(0, 'MBS', p0)

        # Add each BS in the HetNet
        h.add_bs(mbs)

        # Run the HetNet
        h.run(traffic_level[key])
        print(h.evaluation)

        # Instantiate DC Module with DBSCAM algorithm
        dcm = DCM(ClusteringMethod.DBSCAN, PSOAlgorithm.CoPSO, h.ue_list)

        # Run DCM
        dcm.optimization_engine()

        # Collect the generated results
        mean_evolution_list_100_pop_200.append(dcm.optimization_output['CoPSO-DCM-200'])
        mean_evolution_list_100_pop_200_gbest.append(dcm.optimization_output['CoPSO-DCM-200-gbest'])

    # Save the results in CSV files
    # 100% of all UEs and 100 PSO particles
    save_to_csv(mean_evolution_list_100_pop_200, Network.DEFAULT.dir_output_csv,
                "mean_evolution_list_100_pop_200_copso.csv")
    save_to_csv(mean_evolution_list_100_pop_200_gbest, Network.DEFAULT.dir_output_csv,
                "mean_evolution_list_100_pop_200_gbest_copso.csv")
