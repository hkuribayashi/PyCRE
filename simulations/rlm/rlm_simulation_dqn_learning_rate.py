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
    slice_test_filename = os.path.join(GlobalConfig.DEFAULT.rlm_path, "data", "slice_list_computed_{}_{}.obj".format(user_density, n_bs))
    filehandler = open(slice_test_filename, 'rb')
    slice_list = pickle.load(filehandler)

except IOError:
    # Load cluster list
    filename = os.path.join(GlobalConfig.DEFAULT.iom_path, "data", "slice_list_{}_{}_75_pop_400.obj".format(user_density, n_bs))
    filehandler = open(filename, 'rb')
    slice_list = pickle.load(filehandler)

    # Saving the biggest slice for testing pourposes
    slice_list.sort(key=lambda x: len(x.cluster.bs_list), reverse=True)
    for network_slice in slice_list:
        network_slice.compute_selected_bs()

    selected_filename = os.path.join(GlobalConfig.DEFAULT.rlm_path, "data", "slice_list_computed_{}_{}.obj".format(user_density, n_bs))
    filehandler = open(selected_filename, 'wb')
    pickle.dump(slice_list, filehandler)

finally:
    filehandler.close()

learning_rate = [0.5, 0.1, 0.01, 0.001, 0.0001]


original_monitor_value = copy.deepcopy(Monitor.EXT)

for lr in learning_rate:
    mean_satisfaction = []

    config = DQNConfig.DEFAULT
    config.learning_rate = lr

    range_ = len(slice_list)
    range_ = range_ if range_ < 100 else 100

    print("Starting RLM (DQN) - LR {} with {} UEs/km2 and {} BSs/km2".format(lr, user_density, n_bs))
    print("Analysing {} network slice".format(range_))

    for id_slice in range(2):

        # Debug
        print("Slice ID {} - LR {}".format(id_slice, lr))

        # Get the network slice
        network_slice = slice_list[id_slice]

        # Adjusting the Monitor Ext ID
        Monitor.EXT = "{}_{}_{}_{}".format(user_density, lr, id_slice, original_monitor_value)

        full_id = "{}_{}_{}".format(user_density, lr, id_slice)

        # Instantiate the RL Module
        rlm = RLM(full_id, ReinforcementLearningMethod.DQN, network_slice, config)

        # Start the trainning phase and monitor the results
        rlm.learn()
