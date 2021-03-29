import os

from config.Global import GlobalConfig
from utils.charts import get_learning_curve

# Setting avaliable UE density values
user_density = [300]

for density in user_density:
    path_dict = dict()
    learning_rate_list = [0.5, 0.1, 0.01]
    for lr in learning_rate_list:
        lr_path = os.path.join(GlobalConfig.DEFAULT.rlm_path, "csv", "training-{}".format(lr))
        path_dict[lr] = lr_path

    print(path_dict)

    image_path = os.path.join(GlobalConfig.DEFAULT.rlm_path, "images")
    get_learning_curve(path_dict, 4000, image_path, density)
