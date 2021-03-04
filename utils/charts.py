import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from pandas import DataFrame
import seaborn as sns
import pandas as pd

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

    plt.xlim(-1005, 1100)
    plt.ylim(-1005, 1005)
    plt.grid(linestyle='-', linewidth=1, zorder=0, color='#E5E5E5')

    for linha_ue in hetnet.network_element:
        ne_element = [ne_element for ne_element in linha_ue if ne_element.coverage_status is True]
        for ne in ne_element:
            p_ue = [ne.ue.point.x, ne.bs.point.x]
            p_bs = [ne.ue.point.y, ne.bs.point.y]
            plt.plot(p_ue, p_bs, color="black", linewidth=0.5, zorder=5)

    for ue in hetnet.ue_list:
        p = (ue.point.x, ue.point.y)
        ue_circle = plt.Circle(p, 8.5, color="red", zorder=10)
        ax.add_patch(ue_circle)
        if ue.evaluation is False:
            n_ue_circle = plt.Circle(p, 20.5, color="red", zorder=10, fill=False)
            ax.add_patch(n_ue_circle)

    for bs in hetnet.list_bs:
        p = (bs.point.x, bs.point.y)
        if bs.type == 'MBS':
            ue_circle = plt.Circle(p, 13.5, color="blue", zorder=10)
        else:
            ue_circle = plt.Circle(p, 13.5, color="green", zorder=10)
        ax.add_patch(ue_circle)

    plt.show()


def get_evaluation_evolution(data, filename, marker='', xlim=None):
    for key in data:
        plt.plot(data[key][5:149], marker, label=key, markersize=2.2)

    plt.xlabel('Iterations')
    plt.ylabel('Davies-Bouldin Index')
    plt.grid(linestyle=':')
    plt.legend(loc='best')
    if xlim is not None:
        plt.xlim(xlim)

    plt.savefig('{}{}'.format("/Users/hugo/Desktop/PyCRE/images/", filename), dpi=Network.DEFAULT.image_resolution,
                bbox_inches='tight')
    plt.close()


def get_visual_cluster(clustering, data):
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

        xy = data[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=14)

        xy = data[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=6)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()


def get_visual_pareto(data):
    all_points = []
    for d_ in data:
        if d_.evaluation_f1 != 0 and d_.evaluation_f2 != 0:
            point = [(-1) * d_.evaluation_f1, d_.evaluation_f2]
            all_points.append(point)

    df = DataFrame(all_points, columns=['x', 'y'])

    # Make the plot with this subset
    plt.plot('x', 'y', data=df, linestyle='', marker='o')

    # titles
    plt.xlabel('Value of X')
    plt.ylabel('Value of Y')
    plt.title('Overplotting? Sample your data', loc='left')
    plt.show()


def get_boxplot(data_local, data_servidor, path, filename):
    mean_data_local = data_local.mean(axis=0)
    mean_data_servidor = data_servidor.mean(axis=0)

    std_data_local = data_local.std(axis=0)
    std_data_servidor = data_servidor.std(axis=0)



    bar_mean = [mean_data_local['Number of Clusters'], mean_data_servidor['Number of Clusters']]

    se_data_local= std_data_local['Number of Clusters'] / np.sqrt(50)
    se_data_servidor = std_data_servidor['Number of Clusters'] / np.sqrt(50)

    z = 1.96

    lcb_data_local = mean_data_local['Number of Clusters'] - z * se_data_local
    ucb_data_local = mean_data_local['Number of Clusters'] + z * se_data_local

    lcb_data_servidor = mean_data_servidor['Number of Clusters'] - z * se_data_servidor
    ucb_data_servidor = mean_data_servidor['Number of Clusters'] + z * se_data_servidor

    errors = [(lcb_data_local, ucb_data_local), (lcb_data_servidor, ucb_data_servidor)]

    bar_position = [0, 3]

    plt.bar(bar_position, bar_mean, yerr=errors, capsize=7)
    plt.xticks(bar_position, ('Local', 'Servidor'))

    # Save Fig
    plt.savefig('{}{}'.format(path, filename), dpi=Network.DEFAULT.image_resolution, bbox_inches='tight')
    plt.close()
