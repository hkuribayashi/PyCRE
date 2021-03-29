import os
import sys
import copy
import pickle
from stable_baselines3.common.monitor import Monitor

from config.DQNConfig import DQNConfig
from config.Global import GlobalConfig
from modules.rlm.RLM import RLM
from modules.rlm.ReinforcementLearningMethod import ReinforcementLearningMethod

# Get user density
user_density = int(sys.argv[1])

if user_density == 300:
    n_bs = 200
elif user_density == 600:
    n_bs = 400
else:
    n_bs = 800

global filehandler

try:
    slice_test_filename = os.path.join(GlobalConfig.rlm_path, "data", "slice_list_computed_{}_{}.obj".format(user_density, n_bs))
    filehandler = open(slice_test_filename, 'rb')
    slice_list = pickle.load(filehandler)

except IOError:
    # Load cluster list
    filename = os.path.join(GlobalConfig.iom_path, "data", "slice_list_{}_{}_75_pop_400.obj".format(user_density, n_bs))
    filehandler = open(filename, 'rb')
    slice_list = pickle.load(filehandler)

    # Saving the biggest slice for testing pourposes
    slice_list.sort(key=lambda x: len(x.cluster.bs_list), reverse=True)
    for network_slice in slice_list:
        network_slice.compute_selected_bs()

    selected_filename = os.path.join(GlobalConfig.rlm_path, "data", "slice_list_computed_{}_{}.obj".format(user_density, n_bs))
    filehandler = open(selected_filename, 'wb')
    pickle.dump(slice_list, filehandler)

finally:
    filehandler.close()

net_arch_options = dict()
net_arch_options[32] = [32, 32]
net_arch_options[64] = [64, 64]
net_arch_options[128] = [128, 128]

original_monitor_value = copy.deepcopy(Monitor.EXT)

for key in net_arch_options:
    mean_satisfaction = []

    config = DQNConfig.DEFAULT
    config.net_arch = net_arch_options[key]

    # Debug
    print("Starting RLM (DQN) - net_arch {} with {} UEs/km2 and {} BSs/km2".format(net_arch_options[key], user_density, n_bs))

    # Adjusting the Monitor Ext ID
    Monitor.EXT = "{}_{}_{}_{}".format(user_density, key, 0, original_monitor_value)

    # Get the network slice
    network_slice = slice_list[0]

    full_id = "{}_{}_{}".format(user_density, key, 0)

    # Instantiate the RL Module
    rlm = RLM(full_id, ReinforcementLearningMethod.DQN, network_slice, config)

    # Start the trainning phase and monitor the results
    rlm.learn()
