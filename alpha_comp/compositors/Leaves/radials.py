from alpha_comp.compositor import Compositor
import numpy as np
from PIL import Image
import itertools


class Radials(Compositor):

    def composite(self, index, img):
        arr = np.zeros((self.width, self.height, 3))
        radius_space = min(self.width, self.height) / self.limit
        radius_start = radius_space * index
        radius_end = radius_space * (index + 1)

        center_vector = np.array([self.width / 2, self.height / 2])

        pixel_vectors = np.array([[i, j] for i, j in itertools.product(range(self.width), range(self.height)) if i != 0 != j])

        pixel_vectors_center = pixel_vectors - center_vector
        pixel_normals = np.linalg.norm(pixel_vectors_center, axis=1)
        for normal, pixel_vector in zip(pixel_normals, pixel_vectors):
            if radius_start < normal < radius_end:
                arr[pixel_vector[0], pixel_vector[1], :] = 1

        return arr
