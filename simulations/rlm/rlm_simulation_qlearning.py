import os
import sys
import gym
import pickle
from stable_baselines3 import DQN

from config.GlobalConfig import GlobalConfig
from config.network import Network
from modules.dcm.Cluster import Cluster
from modules.iom.Slice import Slice
from network.hetnet import HetNet


simulations = int(sys.argv[1])
user_density = int(sys.argv[2])
max_steps = 100

if user_density == 300:
    n_bs = 200
elif user_density == 600:
    n_bs = 400
else:
    n_bs = 800

satisfaction_result = []
mean_load_result = []

for id_ in range(simulations):
    satisfaction = []
    mean_load = []

    # Create a new HetNet
    h = HetNet(Network.DEFAULT)

    # Create SBS
    h.populate_bs(n_bs)

    # Run the HetNet
    h.run(user_density)
    load = 0
    for bs in h.list_bs:
        load += (bs.load/bs.max_load) * 100
    mean_load_hetnet = load / len(h.list_bs)

    print("Satisfaction: {}".format(h.evaluation["satisfaction"]))
    print("Mean Load: {}".format(mean_load_hetnet))

    satisfaction.append(h.evaluation["satisfaction"])
    mean_load.append(mean_load_hetnet)

    cluster = Cluster(0, h.env.priority_ues_weight, h.env.ordinary_ues_weight, h.env.outage_threshold)
    cluster.bs_list = h.list_bs
    cluster.ue_list = h.ue_list
    network_slice = Slice(cluster, [])
    network_slice.selected_bs = h.list_bs
    cluster.evaluation['satisfaction'] = h.evaluation["satisfaction"]

    gym_env = gym.make("gym_pycre:pycre-v0", network_slice=network_slice)
    policy = dict(net_arch=[64,32,32,20])
    learning_rate = 0.001

    model = DQN("MlpPolicy", gym_env, policy_kwargs=policy, learning_rate=learning_rate, verbose=1)
    model.learn(total_timesteps=10000)
    path = os.path.join(GlobalConfig.DEFAULT.rlm_path, "models", "model_dqn_full_{}.zip".format(id_))
    model.save(path)

    obs = gym_env.reset()
    print(obs)
    step = 0
    while step < max_steps:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = gym_env.step(action)
        print("Step {} - Satisfaction: {}".format(step, info["satisfaction"]))
        satisfaction.append(info["satisfaction"])
        mean_load.append(info["mean_load"])

        step += 1

    print(satisfaction)
    print(mean_load)
    satisfaction_result.append(satisfaction)
    mean_load_result.append(mean_load)

filename = os.path.join(GlobalConfig.DEFAULT.rlm_path, "data", "satisfaction_list_{}_dqn_full.obj".format(user_density))
filehandler = open(filename, 'wb')
pickle.dump(satisfaction_result, filehandler)
filehandler.close()

filename = os.path.join(GlobalConfig.DEFAULT.rlm_path, "data", "mean_load_list_{}_dqn_full.obj".format(user_density))
filehandler = open(filename, 'wb')
pickle.dump(mean_load_result, filehandler)
filehandler.close()

