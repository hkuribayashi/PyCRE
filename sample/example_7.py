import numpy as np

from si.pso.PSO import PSO
from utils.charts import get_visual_cluster
from utils.misc import get_hppp

# X1 = np.array([[1, 2, 1], [2, 2, 1], [2, 3, 1], [8, 7, 0], [8, 8, 0], [25, 80, 0]])

data = get_hppp(1, 1, 5.0, 100)
X1 = np.array(data)
X1 = X1 * 100

p = PSO(X1, 50, 100)
p.search()
print(p.g_best.best_epsilon)
print(p.g_best.best_min_samples)
print(p.g_best.evaluation)
print(p.g_best.total_ues.labels_)

get_visual_cluster(p.g_best.total_ues, X1)

