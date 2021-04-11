import os
import gym
import pickle
from stable_baselines3 import A2C
from stable_baselines3.common.sb2_compat.rmsprop_tf_like import RMSpropTFLike

from config.GlobalConfig import GlobalConfig
from utils.misc import get_mean_load

user_density = 900
n_bs = 800

slice_test_filename = os.path.join(GlobalConfig.DEFAULT.rlm_path, "data", "slice_list_computed_{}_{}.obj".format(user_density, n_bs))
filehandler = open(slice_test_filename, 'rb')
slice_list = pickle.load(filehandler)

print("Number of Slices: {}".format(len(slice_list)))
satisfaction = []
load = []

for id_, network_slice in enumerate(slice_list):
    mean_growth_rate_satisfaction = 0
    satisfaction_list = [network_slice.cluster.evaluation["satisfaction"]]
    load_list = [get_mean_load(network_slice.selected_bs)]

    full_path = os.path.join(GlobalConfig.DEFAULT.rlm_path, "models", "{}_model_a2c_full_{}_2.zip".format(user_density, id_))
    env = gym.make("gym_pycre:pycre-v2", network_slice=network_slice, n_envs=4)

    try:
        model = A2C.load(full_path)
    except FileNotFoundError:
        model = A2C("MlpPolicy", env, verbose=0, policy_kwargs=dict(optimizer_class=RMSpropTFLike, optimizer_kwargs=dict(eps=1e-5)))
        model.learn(total_timesteps=2000)
        model.save(full_path)

    obs = env.reset()
    step = 0

    while step < 100:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        satisfaction_list.append(info["satisfaction"])
        load_list.append(info["mean_load"])
        step += 1
    satisfaction_growth = (max(satisfaction_list) - satisfaction_list[0]) / satisfaction_list[0]
    load_growth = (max(load_list) - load_list[0]) / load_list[0]

    print("ID {}:".format(id_))
    print("Satiscation -  Initial: {} | Final: {} | Growth Rate: {}".format(satisfaction_list[0], max(satisfaction_list), satisfaction_growth * 100))
    print("Mean BS Load - Initial: {} | Final: {} | Growth Rate: {}".format(load_list[0], max(load_list), load_growth * 100))
    print()

    satisfaction.append(satisfaction_list)
    load.append(load_list)

filename = os.path.join(GlobalConfig.DEFAULT.rlm_path, "data", "satisfaction_list_{}_a2c_full.obj".format(user_density))
filehandler = open(filename, 'rb')
pickle.dump(satisfaction, filehandler)
filehandler.close()

filename = os.path.join(GlobalConfig.DEFAULT.rlm_path, "data", "load_list_{}_a2c_full.obj".format(user_density))
filehandler = open(filename, 'rb')
pickle.dump(load, filehandler)
filehandler.close()
