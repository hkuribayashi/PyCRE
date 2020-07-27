import numpy as np


def get_pathloss(type_, distance):
    if type_ == 'MBS':
        pathloss = 128.0 + (37.6 * np.log10(max(distance, 35.0) / 1000.0))
    else:
        pathloss = 140.7 + (36.7 * np.log10((max(distance, 10.0) / 1000.0)))

    return pathloss


def get_distance(point_a, point_b):
    return ((point_b.x - point_a.x) ** 2 + (point_b.y - point_a.y) ** 2 + (point_b.z - point_a.z) ** 2) ** (0.5)


def get_efficiency(sinr):
    if sinr >= 17.6:
        efficiency = 5.55
    elif sinr >= 16.8:
        efficiency = 5.12
    elif sinr >= 15.6:
        efficiency = 4.52
    elif sinr >= 13.8:
        efficiency = 3.9
    elif sinr >= 13.0:
        efficiency = 3.32
    elif sinr >= 11.8:
        efficiency = 2.73
    elif sinr >= 11.4:
        efficiency = 2.41
    elif sinr >= 10.0:
        efficiency = 1.91
    elif sinr >= 6.6:
        efficiency = 1.48
    elif sinr >= 3.0:
        efficiency = 1.18
    elif sinr >= 1.0:
        efficiency = 0.88
    elif sinr >= -1.0:
        efficiency = 0.6
    elif sinr >= -2.6:
        efficiency = 0.38
    elif sinr >= -4.0:
        efficiency = 0.23
    else:
        efficiency = 5.55

    return efficiency