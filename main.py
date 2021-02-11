from clustering.dynamicClustering import DCM
from clustering.method import ClusteringMethod
from config.network import Network
from mobility.point import Point
from network.bs import BS
from network.hetnet import HetNet
from utils.misc import save_to_csv


# traffic_level = {'10': 100}
traffic_level = {'10': 100, '60': 600, '100': 999}

for key in traffic_level:

    # Create a HetNet
    h = HetNet(Network.DEFAULT)

    # Deploy a MBS
    p0 = Point(0.0, 0.0, 35.0)
    mbs = BS(0, 'MBS', p0)

    # Add each BS in the HetNet
    h.add_bs(mbs)

    # Run the HetNet
    h.run(traffic_level[key])
    print(h.evaluation)

    # Start the Dynamic Clustering Module
    mean_evolution_list_10_pop_50 = []
    mean_evolution_list_10_pop_100 = []
    mean_evolution_list_10_pop_200 = []

    mean_evolution_list_10_pop_50_gbest = []
    mean_evolution_list_10_pop_100_gbest = []
    mean_evolution_list_10_pop_200_gbest = []

    mean_evolution_list_60_pop_50 = []
    mean_evolution_list_60_pop_100 = []
    mean_evolution_list_60_pop_200 = []

    mean_evolution_list_60_pop_50_gbest = []
    mean_evolution_list_60_pop_100_gbest = []
    mean_evolution_list_60_pop_200_gbest = []

    mean_evolution_list_100_pop_50 = []
    mean_evolution_list_100_pop_100 = []
    mean_evolution_list_100_pop_200 = []

    mean_evolution_list_100_pop_50_gbest = []
    mean_evolution_list_100_pop_100_gbest = []
    mean_evolution_list_100_pop_200_gbest = []

    # TODO: Incluir o número de repetições na configuração DEFAULT
    for idx in range(50):
        # Instantiate DC Module with DBSCAM algorithm
        dcm = DCM(ClusteringMethod.DBSCAN, h.ue_list)

        # Run DCM
        dcm.optimization_engine()

        # Collect the generated results
        if key is '10':
            # 10% of all UEs and 50 PSO particles
            mean_evolution_list_10_pop_50.append(dcm.optimization_output['PSO-DCM-50'])
            mean_evolution_list_10_pop_50_gbest.append(dcm.optimization_output['PSO-DCM-50-gbest'])

            # 10% of all UEs and 100 PSO particles
            mean_evolution_list_10_pop_100.append(dcm.optimization_output['PSO-DCM-100'])
            mean_evolution_list_10_pop_100_gbest.append(dcm.optimization_output['PSO-DCM-100-gbest'])

            # 10% of all UEs and 200 PSO particles
            mean_evolution_list_10_pop_200.append(dcm.optimization_output['PSO-DCM-200'])
            mean_evolution_list_10_pop_200_gbest.append(dcm.optimization_output['PSO-DCM-200-gbest'])
        elif key is '60':
            # 60% of all UEs and 50 PSO particles
            mean_evolution_list_60_pop_50.append(dcm.optimization_output['PSO-DCM-50'])
            mean_evolution_list_60_pop_50_gbest.append(dcm.optimization_output['PSO-DCM-50-gbest'])

            # 60% of all UEs and 100 PSO particles
            mean_evolution_list_60_pop_100.append(dcm.optimization_output['PSO-DCM-100'])
            mean_evolution_list_60_pop_100_gbest.append(dcm.optimization_output['PSO-DCM-100-gbest'])

            # 60% of all UEs and 200 PSO particles
            mean_evolution_list_60_pop_200.append(dcm.optimization_output['PSO-DCM-200'])
            mean_evolution_list_60_pop_200_gbest.append(dcm.optimization_output['PSO-DCM-200-gbest'])
        elif key is '100':
            #  100% of all UEs and 50 PSO particles
            mean_evolution_list_100_pop_50.append(dcm.optimization_output['PSO-DCM-50'])
            mean_evolution_list_100_pop_50_gbest.append(dcm.optimization_output['PSO-DCM-50-gbest'])

            # 100% of all UEs and 100 PSO particles
            mean_evolution_list_100_pop_100.append(dcm.optimization_output['PSO-DCM-100'])
            mean_evolution_list_100_pop_100_gbest.append(dcm.optimization_output['PSO-DCM-100-gbest'])

            # 100% of all UEs and 200 PSO particles
            mean_evolution_list_100_pop_200.append(dcm.optimization_output['PSO-DCM-200'])
            mean_evolution_list_100_pop_200_gbest.append(dcm.optimization_output['PSO-DCM-200-gbest'])

    # Save the results in CSV files
    if key is '10':
        # 10% of all UEs and 50 PSO particles
        save_to_csv(mean_evolution_list_10_pop_50, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_10_pop_50.csv")
        save_to_csv(mean_evolution_list_10_pop_50_gbest, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_10_pop_50_gbest.csv")

        # 10% of all UEs and 100 PSO particles
        save_to_csv(mean_evolution_list_10_pop_100, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_10_pop_100.csv")
        save_to_csv(mean_evolution_list_10_pop_100_gbest, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_10_pop_100_gbest.csv")

        # 10% of all UEs and 200 PSO particles
        save_to_csv(mean_evolution_list_10_pop_200, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_10_pop_200.csv")
        save_to_csv(mean_evolution_list_10_pop_200_gbest, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_10_pop_200_gbest.csv")
    elif key is '60':
        # 60% of all UEs and 50 PSO particles
        save_to_csv(mean_evolution_list_60_pop_50, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_60_pop_50.csv")
        save_to_csv(mean_evolution_list_60_pop_50_gbest, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_60_pop_50_gbest.csv")

        # 60% of all UEs and 100 PSO particles
        save_to_csv(mean_evolution_list_60_pop_100, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_60_pop_100.csv")
        save_to_csv(mean_evolution_list_60_pop_100_gbest, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_60_pop_100_gbest.csv")

        # 60% of all UEs and 200 PSO particles
        save_to_csv(mean_evolution_list_60_pop_200, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_60_pop_200.csv")
        save_to_csv(mean_evolution_list_60_pop_200_gbest, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_60_pop_200_gbest.csv")
    elif key is '100':
        # 100% of all UEs and 100 PSO particles
        save_to_csv(mean_evolution_list_100_pop_50, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_100_pop_50.csv")
        save_to_csv(mean_evolution_list_100_pop_50_gbest, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_100_pop_50_gbest.csv")

        # 100% of all UEs and 100 PSO particles
        save_to_csv(mean_evolution_list_100_pop_100, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_100_pop_100.csv")
        save_to_csv(mean_evolution_list_100_pop_100_gbest, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_100_pop_100_gbest.csv")

        # 100% of all UEs and 100 PSO particles
        save_to_csv(mean_evolution_list_100_pop_200, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_100_pop_200.csv")
        save_to_csv(mean_evolution_list_100_pop_200_gbest, "/Users/hugo/Desktop/PyCRE/csv/",
                    "mean_evolution_list_100_pop_200_gbest.csv")
