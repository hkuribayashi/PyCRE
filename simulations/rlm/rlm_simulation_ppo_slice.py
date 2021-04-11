import os
import gym
import pickle
from stable_baselines3 import PPO, A2C

from config.GlobalConfig import GlobalConfig

user_density = 900
n_bs = 800

slice_test_filename = os.path.join(GlobalConfig.DEFAULT.rlm_path, "data", "slice_list_computed_{}_{}.obj".format(user_density, n_bs))
filehandler = open(slice_test_filename, 'rb')
slice_list = pickle.load(filehandler)

print("Number of Slices: {}".format(len(slice_list)))
mean_growth_rate_satisfaction = 0
for id_, network_slice in enumerate(slice_list):
    print(network_slice.cluster.evaluation["satisfaction"])
    full_path = os.path.join(GlobalConfig.DEFAULT.rlm_path, "models", "{}_model_a2c_full_{}_2.zip".format(user_density, id_))
    env = gym.make("gym_pycre:pycre-v2", network_slice=network_slice, n_envs=4)

    if os.path.exists(full_path):
        model = A2C.load(full_path)
    else:
        model = A2C("MlpPolicy", env, verbose=1)
        model.learn(total_timesteps=5000)
        model.save(os.path.join(GlobalConfig.DEFAULT.rlm_path, "models", "{}_model_a2c_full_{}_2.zip".format(user_density, id_)))

    obs = env.reset()
    step = 0
    satisfaction_list = []
    satisfaction_list.append(network_slice.cluster.evaluation["satisfaction"])
    while step < 100:
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        satisfaction_list.append(info["satisfaction"])
        step += 1
    mean = (satisfaction_list[-1] - satisfaction_list[0]) / satisfaction_list[0]
    print("ID {} - Inicial: {} | Final: {} | Crescimento: {}".format(id_, satisfaction_list[0], satisfaction_list[-1], mean * 100))
    mean_growth_rate_satisfaction += mean

mean_growth_rate_satisfaction = mean_growth_rate_satisfaction/len(slice_list)
print(mean_growth_rate_satisfaction * 100)
