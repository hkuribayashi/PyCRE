import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.cluster import DBSCAN


from config.network import Network

def get_visual(hetnet):

    # Legend
    legend_elements = [Line2D([0], [0], marker='o', color='w', label='MBS', markerfacecolor='b', markersize=10),
                       Line2D([0], [0], marker='o', color='w', label='SBS', markerfacecolor='g', markersize=10),
                       Line2D([0], [0], marker='o', color='w', label='UE', markerfacecolor='r', markersize=10)]

    # Create figure
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.legend(handles=legend_elements, loc='best')

    plt.xlim(-105, 105)
    plt.ylim(-105, 105)
    plt.grid(linestyle='-', linewidth=1, zorder=0, color='#E5E5E5')

    for coluna in map(list, zip(*hetnet.network_element)):
        lista_ne = [element for element in coluna if element.coverage_status is True]
        for ne in lista_ne:
            p_ue = [ne.ue.point.x, ne.bs.point.x]
            p_bs = [ne.ue.point.y, ne.bs.point.y]
            plt.plot(p_ue, p_bs, color="black", linewidth=0.5, zorder=5)

    for ue in hetnet.ue_list:
        p = (ue.point.x, ue.point.y)
        ue_circle = plt.Circle(p, 1.5, color="red", zorder=10)
        ax.add_patch(ue_circle)
        if ue.evaluation is False:
            n_ue_circle = plt.Circle(p, 3.5, color="red", zorder=10, fill=False)
            ax.add_patch(n_ue_circle)

    for bs in hetnet.list_bs:
        p = (bs.point.x, bs.point.y)
        if bs.type == 'MBS':
            ue_circle = plt.Circle(p, 3.5, color="blue", zorder=10)
        else:
            ue_circle = plt.Circle(p, 2.5, color="green", zorder=10)
        ax.add_patch(ue_circle)

    plt.show()


def get_evaluation_evolution(data):
    for key in data:
        plt.plot(data[key], '-*', label=key)
        # plt.plot(data, '-*', label='PSO-DCM', color='#1F77B4')

    plt.xlabel('Iterations')
    plt.ylabel('Davies-Bouldin Index')
    plt.grid(linestyle=':')
    plt.legend(loc='best')

    plt.savefig('{}Mean-Evaluation-Evolution.eps'.format(Network.DEFAULT.dir_output_images), dpi=Network.DEFAULT.image_resolution, bbox_inches='tight')
    plt.close()



def get_visual_cluster(pso_gbest, X):
    clustering = DBSCAN(eps=pso_gbest.best_epsilon, min_samples=pso_gbest.best_min_samples).fit(X)
    labels = clustering.labels_
    core_samples_mask = np.zeros_like(clustering.labels_, dtype=bool)
    core_samples_mask[clustering.core_sample_indices_] = True
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=14)

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=6)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
