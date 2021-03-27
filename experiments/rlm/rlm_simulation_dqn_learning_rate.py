import sys
import copy
import pickle
from stable_baselines3.common.monitor import Monitor

from config.DQNConfig import DQNConfig
from modules.rlm.RLM import RLM
from modules.rlm.ReinforcementLearningMethod import ReinforcementLearningMethod


# Get user density
user_density = int(sys.argv[1])

# Get number of BSs
n_bs = int(sys.argv[2])

# Get the path to save results
path = sys.argv[3]

global filehandler

try:
    slice_test_filename = "/Users/hugo/Desktop/PyCRE/rlm/data/slice_list_computed_{}_{}.obj".format(user_density, n_bs)
    filehandler = open(slice_test_filename, 'rb')
    slice_list = pickle.load(filehandler)

except IOError:
    # Load cluster list
    filename = "/Users/hugo/Desktop/PyCRE/iom/data/slice_list_{}_{}_75_pop_400.obj".format(user_density, n_bs)
    filehandler = open(filename, 'rb')
    slice_list = pickle.load(filehandler)

    # Saving the biggest slice for testing pourposes
    slice_list.sort(key=lambda x: len(x.cluster.bs_list), reverse=True)
    for network_slice in slice_list:
        network_slice.compute_selected_bs()

    selected_filename = "/Users/hugo/Desktop/PyCRE/rlm/data/slice_list_computed_{}_{}.obj".format(user_density, n_bs)
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

    # Debug
    print("Starting RLM (DQN) - LR {} with {} UEs/km2 and {} BSs/km2".format(lr, user_density, n_bs))

    # Adjusting the Monitor Ext ID
    Monitor.EXT = "{}_{}_{}_{}".format(user_density, lr, 0, original_monitor_value)

    # Get the network slice
    network_slice = slice_list[0]

    full_id = "{}_{}_{}".format(user_density, lr, 0)

    # Instantiate the RL Module
    rlm = RLM(full_id, ReinforcementLearningMethod.DQN, network_slice, config)

    # Start the trainning phase and monitor the results
    rlm.learn()
