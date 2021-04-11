import os

from config.GlobalConfig import GlobalConfig
from utils.charts import moving_average, get_training_steps_curve
from utils.misc import load_from_csv_number

user_density = 900
window = 50
max_x = 1000
csv_path = os.path.join(GlobalConfig.DEFAULT.rlm_path, "csv")

# 0: [64, 32, 32, 64]
id_ = "4_neurons_{}".format(0)
filename_0 = "rlm_dqn_episode_rewards_{}_{}.csv".format(user_density, id_)
data_0 = load_from_csv_number(csv_path, filename_0, 1000)
data_0.fillna(0)
data_0 = data_0.mean(axis=0)
mean_data_0 = moving_average(data_0, window)

# 1: [64, 64, 64, 20]
id_ = "4_neurons_{}".format(1)
filename_1 = "rlm_dqn_episode_rewards_{}_{}.csv".format(user_density, id_)
data_1 = load_from_csv_number(csv_path, filename_1, 1000)
data_1.fillna(0)
data_1 = data_1.mean(axis=0)
mean_data_1 = moving_average(data_1, window)

# 2: [64, 64, 64, 32]
id_ = "4_neurons_{}".format(2)
filename_3 = "rlm_dqn_episode_rewards_{}_{}.csv".format(user_density, id_)
data_3 = load_from_csv_number(csv_path, filename_3, 1000)
data_3.fillna(0)
data_3 = data_3.mean(axis=0)
mean_data_2 = moving_average(data_3, window)

# 3: [64, 32, 32, 20]
id_ = "4_neurons_{}".format(3)
filename_3 = "rlm_dqn_episode_rewards_{}_{}.csv".format(user_density, id_)
data_3 = load_from_csv_number(csv_path, filename_3, 1000)
data_3.fillna(0)
data_3 = data_3.mean(axis=0)
mean_data_3 = moving_average(data_3, window)

data = {"Neurons [64, 32, 32, 64]": mean_data_0[0:max_x],
        "Neurons [64, 64, 64, 20]": mean_data_1[0:max_x],
        "Neurons [64, 64, 64, 32]": mean_data_2[0:max_x],
        "Neurons [64, 32, 32, 20]": mean_data_3[0:max_x]}

image_path = os.path.join(GlobalConfig.DEFAULT.rlm_path, "images", "{}_neurons_episode_rewards.eps".format(user_density))
get_training_steps_curve(data, image_path, xlabel="Episodes", ylabel="Smoothing Obtained Rewards")
