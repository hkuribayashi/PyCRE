import numpy as np

from mobilitymodel.basic import Point, ApplicationProfile


def get_hppp(density, area, height):
    lower = 0.0
    upper = area**(0.5)
    points = (int) (density * area)

    x = np.random.uniform(lower, upper, points)

    y = np.random.uniform(lower, upper, points)

    for i in x:
        points = Point(x[i], y[i], height)

    return points