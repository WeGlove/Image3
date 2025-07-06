from src.math.Geos import get_centered_vector_map
import torch
import math


def linear_dist(a, b, width, height, device):
    vector_map = get_centered_vector_map(width, height, device)

    vector_map = vector_map * position[:2]
    vector_map = torch.sum(vector_map, dim=2)
    vector_map = vector_map + position[2]
    vector_map = vector_map / math.sqrt(position[0] ** 2 + position[1] ** 2)
    vector_map = vector_map / math.sqrt((width / 2) ** 2 + (height / 2) ** 2)
    vector_map = torch.abs(vector_map)

    vector_map += shift

    return vector_map


def linear(a, x, b):
    """
    Computes ax+b
    :param a:
    :param x:
    :param b:
    :return:
    """
    return a * x + b


def point_slope_to_linear(x, a):
    return a, x[1] - a * x[0]


def two_points_to_linear(x0, x1, position):
    x0_x1 = x1-x0
    a = math.sqrt(x0_x1[0]**2 + x0_x1[1]**2)
    return point_slope_to_linear(position, a)

