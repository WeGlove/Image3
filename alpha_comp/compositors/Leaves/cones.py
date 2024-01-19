from alpha_comp.compositor import Compositor
import numpy as np
from PIL import Image
import itertools


class Cones(Compositor):

    def composite(self, width, height, index, limit, arg):
        arr = np.zeros((width, height, 3))
        angle_space = 360 / limit
        angle_start = angle_space * index
        angle_end = angle_space * (index + 1)

        center_vector = np.array([width / 2, height / 2])

        pixel_vectors = np.array([[i, j] for i, j in itertools.product(range(width), range(height)) if i != 0 != j])

        pixel_vectors_center = pixel_vectors - center_vector
        pixel_normals = np.array([pixel_vectors_center[:, 0] / np.linalg.norm(pixel_vectors_center, axis=1),
                                  pixel_vectors_center[:, 1] / np.linalg.norm(pixel_vectors_center, axis=1)]).T
        normal = np.array([1, 0])
        alpha = np.cross(pixel_normals, normal)
        alpha = np.arcsin(alpha) / np.pi * 180 + 90
        for alpha_value, pixel_vector in zip(alpha, pixel_vectors):
            if (pixel_vector - center_vector)[0] < 0:
                alpha_value += 180
            if angle_start < alpha_value < angle_end:
                arr[pixel_vector[0], pixel_vector[1], :] = 1

        return arr, None
