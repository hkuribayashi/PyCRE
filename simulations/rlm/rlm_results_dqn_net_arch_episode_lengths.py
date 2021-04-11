import os

from config.GlobalConfig import GlobalConfig
from utils.charts import moving_average, get_training_steps_curve
from utils.misc import load_from_csv_number

user_density = 900
window = 50
max_x = 1000
csv_path = os.path.join(GlobalConfig.DEFAULT.rlm_path, "csv")

# 2 layers
filename_2 = "rlm_dqn_episode_lengths_{}_2_hl.csv".format(user_density)
data_2hl = load_from_csv_number(csv_path, filename_2, 1000)
data_2hl.fillna(0)
data_2hl = data_2hl.mean(axis=0)
mean_data_2hl = moving_average(data_2hl, window)

# 3 layers
filename_3 = "rlm_dqn_episode_lengths_{}_3_hl.csv".format(user_density)
data_3hl = load_from_csv_number(csv_path, filename_3, 1000)
data_3hl.fillna(0)
data_3hl = data_3hl.mean(axis=0)
mean_data_3hl = moving_average(data_3hl, window)

# 4 layers
filename_4 = "rlm_dqn_episode_lengths_{}_4_hl.csv".format(user_density)
data_4hl = load_from_csv_number(csv_path, filename_4, 1000)
data_4hl.fillna(0)
data_4hl = data_4hl.mean(axis=0)
mean_data_4hl = moving_average(data_4hl, window)

data = {"2 layers [32,32]": mean_data_2hl[0:max_x],
        "3 layers [64,32,32]": mean_data_3hl[0:max_x],
        "4 layers [64,32,32,20]": mean_data_4hl[0:max_x]}

path = os.path.join(GlobalConfig.DEFAULT.rlm_path, "images", "{}_net_arch_episode_lengths.eps".format(user_density))
get_training_steps_curve(data, path, ylabel="Smoothing Training Steps")