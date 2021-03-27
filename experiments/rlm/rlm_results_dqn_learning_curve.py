import sys
import pandas as pd

from utils.charts import get_mean_evaluation_cluster


# Get user density
user_density = int(sys.argv[1])

# Get number of BSs
n_bs = int(sys.argv[2])

# CVS Path
path = sys.argv[3]

chart_data = {}

# Q-Learning
data_ = []
csv_filename = 'rlm_qlearning_300_200-2.csv'.format(user_density, n_bs)
data = pd.read_csv('{}{}'.format(path, csv_filename), header=None, delimiter=',', sep=',')
data_.append(data)
chart_data["Q-Learning"] = pd.concat(data_).mean(axis=0)

# Q-Learning
data_ = []
csv_filename = 'rlm_dqn_300_200.csv'.format(user_density, n_bs)
data = pd.read_csv('{}{}'.format(path, csv_filename), header=None, delimiter=',', sep=',')
data_.append(data)
chart_data["DQN-300"] = pd.concat(data_).mean(axis=0)

# DQN
data_ = []
csv_filename = 'rlm_dqn_600_400.csv'.format(user_density, n_bs)
data = pd.read_csv('{}{}'.format(path, csv_filename), header=None, delimiter=',', sep=',')
data_.append(data)
chart_data["DQN-600"] = pd.concat(data_).mean(axis=0)

# DQN
data_ = []
csv_filename = 'rlm_dqn_900_800.csv'.format(user_density, n_bs)
data = pd.read_csv('{}{}'.format(path, csv_filename), header=None, delimiter=',', sep=',')
data_.append(data)
chart_data["DQN-900"] = pd.concat(data_).mean(axis=0)

get_mean_evaluation_cluster(chart_data, 'rlm_mean_satisfaction_per_cluster_{}.eps'.format(user_density), '-*')
