from utils.charts import get_evaluation_evolution
from utils.misc import consolidate_results

path = "/Users/hugo/Desktop/PyCRE/csv/"

# traffic_level = {'10': 100, '60': 600, '100': 999}
traffic_level = {'10': 100, '60': 600}
population_size = [50, 100, 200]
chart_data = {}

# # Plot mean evalution evolution
# for key in traffic_level:
#     chart_data = {}
#     for population in population_size:
#         csv_filename = 'mean_evolution_list_{}_pop_{}.csv'.format(key, population)
#         img_filename = 'mean_evolution_list_{}.eps'.format(key)
#         mean_data = consolidate_results(path, csv_filename)
#         chart_data[population] = mean_data
#     get_evaluation_evolution(chart_data, img_filename, '-*')
#
# # Plot gbest evalution evolution
# for key in traffic_level:
#     chart_data = {}
#     for population in population_size:
#         csv_filename = 'mean_evolution_list_{}_pop_{}_gbest.csv'.format(key, population)
#         img_filename = 'mean_evolution_list_{}_gbest.eps'.format(key)
#         mean_data = consolidate_results(path, csv_filename)
#         chart_data[population] = mean_data
#     get_evaluation_evolution(chart_data, img_filename)

chart_data = {}
csv_filename = "mean_evolution_10_pop_50_gbest_DCMPSO.csv"

img_filename = "teste.eps"
mean_data = consolidate_results(path, csv_filename)

chart_data["remoto"] = mean_data

get_evaluation_evolution(chart_data, img_filename, '-*')
