import numpy as np


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_distance(self, point):
        return ((self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2) ** (0.5)

    def __str__(self):
        return '[x={}, y={}, z={}]'.format(self.x, self.y, self.z)


def get_hppp(density, area, height):
    lower = 0.0
    upper = area ** (0.5)
    points = (int)(density * area)
    list = []

    x = np.random.uniform(lower, upper, points)
    y = np.random.uniform(lower, upper, points)

    for (i, j) in zip(x, y):
        list.append(Point(i, j, height))

    return list
