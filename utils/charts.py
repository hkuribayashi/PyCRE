import matplotlib.pyplot as plt


def get_visual(hetnet):
    # Create figure
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    plt.xlim(-105, 105)
    plt.ylim(-105, 105)
    plt.grid(linestyle='-', linewidth=1, zorder=0, color='#E5E5E5')

    for coluna in map(list, zip(*hetnet.network_element)):
        lista_ne = [element for element in coluna if element.coverage_status is True]
        for ne in lista_ne:
            p_ue = [ne.ue.point.x, ne.bs.point.x]
            p_bs = [ne.ue.point.y, ne.bs.point.y]
            plt.plot(p_ue, p_bs, color="black", linewidth=0.5, zorder=5)

    for ue in hetnet.list_ue:
        p = (ue.point.x, ue.point.y)
        ue_circle = plt.Circle(p, 1.5, color="red", zorder=10)
        ax.add_patch(ue_circle)
        if ue.evaluation is False:
            n_ue_circle = plt.Circle(p, 3.5, color="red", zorder=10, fill=False)
            ax.add_patch(n_ue_circle)

    for bs in hetnet.list_bs:
        p = (bs.point.x, bs.point.y)
        ue_circle = plt.Circle(p, 1.5, color="blue", zorder=10)
        ax.add_patch(ue_circle)

    plt.show()
