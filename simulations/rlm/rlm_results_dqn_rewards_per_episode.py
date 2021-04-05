import os

from config.GlobalConfig import GlobalConfig
from utils.charts import moving_average, get_episode_rewards_curve
from utils.misc import load_from_csv_number

window = 60
max_x = 1000
path = "/Users/hugo/Desktop/PyCRE/rlm/csv/"

# 0.0001
filename_0001 = "rlm_dqn_episode_rewards_900_0.0001.csv"
data_0001 = load_from_csv_number(path, filename_0001, 1000)
data_0001.fillna(0)
data_0001 = data_0001.mean(axis=0)
mean_data_0001 = moving_average(data_0001, window)

# 0.001
filename_001 = "rlm_dqn_episode_rewards_900_0.001.csv"
data_001 = load_from_csv_number(path, filename_001, 1000)
data_001.fillna(0)
data_001 = data_001.mean(axis=0)
mean_data_001 = moving_average(data_001, window)

# 0.01
filename_01 = "rlm_dqn_episode_rewards_900_0.01.csv"
data_01 = load_from_csv_number(path, filename_01, 1000)
data_01.fillna(0)
data_01 = data_01.mean(axis=0)
mean_data_01 = moving_average(data_01, window)

# 0.1
filename_1 = "rlm_dqn_episode_rewards_900_0.1.csv"
data_1 = load_from_csv_number(path, filename_1, 1000)
data_1.fillna(0)
data_1 = data_1.mean(axis=0)
mean_data_1 = moving_average(data_1, window)

data = {"0.1": mean_data_1[0:max_x], "0.01": mean_data_01[0:max_x], "0.001": mean_data_001[0:max_x], "0.0001": mean_data_0001[0:max_x]}
path = os.path.join(GlobalConfig.DEFAULT.rlm_path, "images")
get_episode_rewards_curve(data, path, "900")
