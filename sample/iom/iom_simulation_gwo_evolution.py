import pandas as pd

from utils.charts import get_evaluation_evolution


weight_list = [0.9, 0.5, 0.1]

# CVS Path
path = "/Users/hugo/Desktop/PyCRE/iom/csv/"

chart_data = {}
for weight in weight_list:

    # 300/200
    data_per_weight = []
    for id_ in range(0, 61):
        csv_filename = 'iom_300_cluster_mean_evolution_{}_pop_200_GWO_{}.csv'.format(weight, id_)
        data = pd.read_csv('{}{}'.format(path, csv_filename), header=None, delimiter=',', sep=',')
        data_per_weight.append(data)
    chart_data["300-200"] = pd.concat(data_per_weight).mean(axis=0)

    # 600/400
    data_per_weight = []
    for id_ in range(0, 61):
        csv_filename = 'iom_300_cluster_mean_evolution_{}_pop_200_GWO_{}.csv'.format(weight, id_)
        data = pd.read_csv('{}{}'.format(path, csv_filename), header=None, delimiter=',', sep=',')
        data_per_weight.append(data)
    chart_data["600-400"] = pd.concat(data_per_weight).mean(axis=0)

    # 900/800
    data_per_weight = []
    for id_ in range(0, 61):
        csv_filename = 'iom_300_cluster_mean_evolution_{}_pop_200_GWO_{}.csv'.format(weight, id_)
        data = pd.read_csv('{}{}'.format(path, csv_filename), header=None, delimiter=',', sep=',')
        data_per_weight.append(data)
    chart_data["900-800"] = pd.concat(data_per_weight).mean(axis=0)

    # Plot
    get_evaluation_evolution(chart_data, 'iom_gwo_evolution_{}.eps'.format(weight), '-*', (0, 300))
