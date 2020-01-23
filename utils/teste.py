import numpy as np

from mobilitymodel.basic import Point, ApplicationProfile


def get_hppp(density, area, height):
    lower = 0.0
    upper = area**(0.5)
    points = (int) (density * area)
    list = []

    x = np.random.uniform(lower, upper, points)
    y = np.random.uniform(lower, upper, points)

    for (i,j) in zip(x, y):
        list.append(Point(i, j, height))

    return list