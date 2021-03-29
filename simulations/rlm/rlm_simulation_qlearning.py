import sys
import pickle

from config.QLConfig import QLConfig
from algorithms.rl.qlearning.Environment import Environment
from algorithms.rl.qlearning.QLSingleAgent import QLSigleAgent
from modules.rlm.RLM import RLM
from modules.rlm.ReinforcementLearningMethod import ReinforcementLearningMethod
from utils.misc import save_to_csv


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
    # slice_list.sort(key=lambda x: len(x.cluster.bs_list), reverse=True)
    for slice_ in slice_list:
        slice_.compute_selected_bs()

    selected_filename = "/Users/hugo/Desktop/PyCRE/rlm/data/slice_list_computed_{}_{}.obj".format(user_density, n_bs)
    filehandler = open(selected_filename, 'wb')
    pickle.dump(slice_list, filehandler)

finally:
    filehandler.close()

# Setting reinforcement Learning configs
config = QLConfig.DEFAULT
config.verbose = False

# Mean Evaluation for all Slices
# 101: Number of episodes + the inicial cluster evaluation
mean_satisfaction = []

size = len(slice_list)
range_ = size if size < 50 else 50

# Debug
print("Starting RLM (Q-Learning) with {} UEs/km2 and {} BSs/km2".format(user_density, n_bs))
print("Analysing {} network slices".format(size))

for id_ in range(size):
    slice_ = slice_list[id_]
    print("Slice Index {}".format(id_))
    rlm = RLM(rl_method=ReinforcementLearningMethod.QLEARNING, network_slice=slice_, config=config)
    rlm.run()
    mean_satisfaction.append(rlm.evaluation["satisfaction"])
    print(rlm.evaluation["satisfaction"])

# Compute mean and save results
save_to_csv(list(mean_satisfaction), path, "rlm_qlearning_{}_{}.csv".format(user_density, n_bs))
