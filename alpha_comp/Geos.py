import numpy as np
import itertools


def radial(width, height, radius_low, radius_high):
    arr = np.ones((width, height))

    center_vector = np.array([width / 2, height / 2])
    pixel_vectors = np.mgrid[0:width, 0:height].transpose((1, 2, 0))

    pixel_vectors_center = pixel_vectors - center_vector
    pixel_normals = np.linalg.norm(pixel_vectors_center, axis=-1)

    arr[pixel_normals > radius_high] = 0
    arr[pixel_normals < radius_low] = 0

    arr = np.array([arr, arr, arr]).transpose((1, 2, 0))

    return arr
