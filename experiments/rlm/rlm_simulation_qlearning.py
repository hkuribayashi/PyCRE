import sys
import pickle
import numpy as np

from config.qlearning import Agent
from rl.qlearning.env import Environment
from rl.qlearning.agent import SingleAgent
from utils.misc import save_to_csv


# Get user density
user_density = int(sys.argv[1])

# Get number of BSs
n_bs = int(sys.argv[2])

# Get the number of repetitions
n_repetitions = int(sys.argv[3])

# Get the path to save results
path = sys.argv[4]

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
    for slice_ in slice_list:
        slice_.compute_selected_bs()

    selected_filename = "/Users/hugo/Desktop/PyCRE/rlm/data/slice_list_computed_{}_{}.obj".format(user_density, n_bs)
    filehandler = open(selected_filename, 'wb')
    pickle.dump(slice_list, filehandler)

finally:
    filehandler.close()

# Setting reinforcement Learning configs
config = Agent.DEFAULT
config.verbose = False

# Mean Evaluation for all Slices
# 101: Number of episodes + The Inicial Cluster Evaluation
mean_evaluation = np.zeros(101)

# Debug
print("Starting RLM with {} UEs/km2 and {} BSs/km2".format(user_density, n_bs))
print("Analysing {} network slices".format(len(slice_list)))

# For each slice invoke Q-learning Engine
# Repetitions: Run 'n_repetitions' times each slice

for id_, slice_ in enumerate(slice_list):
    print("Slice Index {}".format(id_))
    counter = 0
    while counter < n_repetitions:
        env = Environment(slice_)
        sigle_agent = SingleAgent(env, Agent.DEFAULT)
        sigle_agent.run()
        mean_evaluation += np.array(sigle_agent.satisfaction_all_episodes)
        print(sigle_agent.satisfaction_all_episodes)
        counter += 1

# Compute mean and save results
mean_evaluation = mean_evaluation/len(slice_list)
save_to_csv(mean_evaluation, path, "rlm_qlearning_{}_{}.csv".format(user_density, n_bs))
