from src.math.gemoetry import get_centered_vector_map
import torch
import math


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

