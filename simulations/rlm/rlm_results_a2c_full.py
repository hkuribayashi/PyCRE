import os
import gym
import pickle

from stable_baselines3 import DQN, A2C

from config.GlobalConfig import GlobalConfig

user_density = [300, 600]

for density in user_density:
    print("User Density: {}".format(density))
    path = os.path.join(GlobalConfig.DEFAULT.rlm_path, "data", "satisfaction_list_{}_dqn_full.obj".format(density))
    filehandler = open(path, 'rb')
    satisfaction_list = pickle.load(filehandler)
    mean_growth_rate_satisfaction = 0
    for satisfaction in satisfaction_list:
        mean_growth_rate_satisfaction += (satisfaction[-1] - satisfaction[0]) / satisfaction[0]
    mean_growth_rate_satisfaction = mean_growth_rate_satisfaction / len(satisfaction_list)
    print("Mean Growth Rate: {}".format(mean_growth_rate_satisfaction * 100))

    path = os.path.join(GlobalConfig.DEFAULT.rlm_path, "data", "mean_load_list_{}_dqn_full.obj".format(density))
    filehandler = open(path, 'rb')
    mean_load_list = pickle.load(filehandler)
    mean_growth_rate_load = 0
    for mean_load in mean_load_list:
        mean_growth_rate_load += (mean_load[-1] - mean_load[0]) / mean_load[0]
    mean_growth_rate_load = mean_growth_rate_load / len(mean_load_list)
    print("Mean BS Load: {}".format(mean_growth_rate_load * 100))

print("\n")

user_density = 900

if user_density == 300:
    n_bs = 200
elif user_density == 600:
    n_bs = 400
else:
    n_bs = 800

slice_test_filename = os.path.join(GlobalConfig.DEFAULT.rlm_path, "data", "slice_list_computed_{}_{}.obj".format(user_density, n_bs))
filehandler = open(slice_test_filename, 'rb')
slice_list = pickle.load(filehandler)

print("Number of Slices: {}".format(len(slice_list)))
mean_growth_rate_satisfaction = 0
for id_, network_slice in enumerate(slice_list):
    print(network_slice.cluster.evaluation["satisfaction"])
    env = gym.make("gym_pycre:pycre-v1", network_slice=network_slice)
    model = A2C("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000)
    model.save(os.path.join(GlobalConfig.DEFAULT.rlm_path, "models", "{}_model_a2c_full_{}".format(user_density, id_)))

    obs = env.reset()
    step = 0
    satisfaction_list = []
    satisfaction_list.append(network_slice.cluster.evaluation["satisfaction"])
    while step < 100:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        satisfaction_list.append(info["satisfaction"])
        step += 1
    mean = (satisfaction_list[-1] - satisfaction_list[0]) / satisfaction_list[0]
    print("ID {} - Inicial: {} | Final: {} | Crescimento: {}".format(id_, satisfaction_list[0], satisfaction_list[-1], mean * 100))
    mean_growth_rate_satisfaction += mean

mean_growth_rate_satisfaction = mean_growth_rate_satisfaction/len(slice_list)
print(mean_growth_rate_satisfaction * 100)
