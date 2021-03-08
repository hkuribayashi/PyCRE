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


def get_barchart(cluster_data, path, z=1.64):
    clusters_bar = []
    samples_bar = []
    outliers_bar = []

    error_cluster = []
    error_samples = []
    error_outliers = []

    for c_data in cluster_data:
        # Get Mean and Standard Deviation
        mean = c_data.mean(axis=0)
        std = c_data.std(axis=0)

        # Append data
        clusters_bar.append(mean['Number of Clusters'])
        samples_bar.append(mean['Number of Samples per Clusters'])
        outliers_bar.append(mean['Number of Outliers'])

        # Compute SE and CI
        # Number of Clusters
        se_clusters = std['Number of Clusters']/np.sqrt(len(c_data))
        lcb_clusters = mean['Number of Clusters'] - z * se_clusters
        ucb_clusters = mean['Number of Clusters'] + z * se_clusters
        error_cluster.append((lcb_clusters, ucb_clusters))

        # Number of Samples per Clusters
        se_samples = std['Number of Samples per Clusters'] / np.sqrt(len(c_data))
        lcb_samples = mean['Number of Samples per Clusters'] - z * se_samples
        ucb_samples = mean['Number of Samples per Clusters'] + z * se_samples
        error_samples.append((lcb_samples, ucb_samples))

        # Number of Outliers
        se_outliers = std['Number of Outliers'] / np.sqrt(len(c_data))
        lcb_outliers = mean['Number of Outliers'] - z * se_outliers
        ucb_outliers = mean['Number of Outliers'] + z * se_outliers
        error_outliers.append((lcb_outliers, ucb_outliers))

    bar_position = [0, 1.5, 3, 4.5]

    # Clusters
    # plt.bar(bar_position, clusters_bar, yerr=error_cluster, capsize=7, width=0.5, zorder=10)
    plt.bar(bar_position, clusters_bar, capsize=7, width=0.5, zorder=10)
    plt.xticks(bar_position, ('300', '600', '900', '1200'))
    plt.xlabel('Mean User Density [UE/km2]')
    plt.ylabel('Mean Number of Clusters')
    plt.grid(linestyle=':', zorder=1)
    plt.savefig('{}{}'.format(path, "mean_number_of_clusters.eps"), dpi=Network.DEFAULT.image_resolution, bbox_inches='tight')

    # Samples
    plt.figure()
    # plt.bar(bar_position, samples_bar, yerr=error_samples, capsize=7, width=0.5, zorder=10)
    plt.bar(bar_position, samples_bar, capsize=7, width=0.5, zorder=10)
    plt.xticks(bar_position, ('300', '600', '900', '1200'))
    plt.xlabel('Mean User Density [UE/km2]')
    plt.ylabel('Mean Number of Samples per Clusters')
    plt.grid(linestyle=':', zorder=1)
    plt.savefig('{}{}'.format(path, "mean_number_of_samples_per_cluster.eps"), dpi=Network.DEFAULT.image_resolution, bbox_inches='tight')

    # Outliers
    plt.figure()
    # plt.bar(bar_position, outliers_bar, yerr=error_outliers, capsize=7, width=0.5, zorder=10)
    plt.bar(bar_position, outliers_bar, capsize=7, width=0.5, zorder=10)
    plt.xticks(bar_position, ('300', '600', '900', '1200'))
    plt.xlabel('Mean User Density [UE/km2]')
    plt.ylabel('Mean Number of Outliers')
    plt.grid(linestyle=':', zorder=1)
    plt.savefig('{}{}'.format(path, "mean_number_of_outliers.eps"), dpi=Network.DEFAULT.image_resolution, bbox_inches='tight')
