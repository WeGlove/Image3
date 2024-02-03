import numpy as np
import itertools


def radial(width, height, radius_low, radius_high):
    arr = np.zeros((width, height, 3))

    center_vector = np.array([width / 2, height / 2])

    pixel_vectors = np.array(
        [[i, j] for i, j in itertools.product(range(width), range(height)) if i != 0 != j])

    pixel_vectors_center = pixel_vectors - center_vector
    pixel_normals = np.linalg.norm(pixel_vectors_center, axis=1)
    for normal, pixel_vector in zip(pixel_normals, pixel_vectors):
        if radius_low < normal < radius_high:
            arr[pixel_vector[0], pixel_vector[1], :] = 1

    return arr
