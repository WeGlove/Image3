import itertools

import numpy as np
from alpha_comp.compositor import Compositor


class TransformationHomoMatrix(Compositor):

    def __init__(self, compositor, mat):
        super().__init__()
        self.compositor = compositor
        self.mat = mat

    def initialize(self, width, height, limit):
        super().initialize(width, height, limit)
        self.compositor.initialize(width, height, limit)

    def composite(self, index, img):
        mask = np.zeros((self.width, self.height, 3))
        mask_out = self.compositor.composite(index, img)
        for x, y in itertools.product(range(self.width), range(self.height)):
            vec = self.mat @ np.array([x, y, 1])
            if vec[2] == 0:
                vec = [0, 0]
            else:
                vec = [(int(vec[0] / vec[2]) % self.width), int(vec[1] / vec[2]) % self.height]
            #print(x, y, vec, mask.shape, mask_out.shape)
            mask[x, y, :] = mask_out[vec[0], vec[1], :]
        return mask

    @staticmethod
    def scale(x, y):
        return np.array([[x, 0, 0], [0, y, 0], [0, 0, 1]])

    @staticmethod
    def squeeze(k):
        return TransformationHomoMatrix.scale(k, 1/k)

    @staticmethod
    def shear_x(x):
        return np.array([[1, np.tan(x), 1], [0, 1, 0], [0, 0, 1]])

    @staticmethod
    def shear_y(y):
        return np.array([[1, 0, 0], [np.tan(y), 1, 0], [0, 0, 1]])

    @staticmethod
    def rotation_2D(phi):
        return np.array([[np.cos(phi), -np.sin(phi), 0], [np.sin(phi), np.cos(phi),0 ], [0, 0, 1]])

    @staticmethod
    def perspective_projection_y(y=1):
        return np.array([[1, 0, 0], [0, 1, 0], [0, y, 0]])

    @staticmethod
    def perspective_projection_x(x=1):
        return np.array([[1, 0, 0], [0, 1, 0], [x, 0, 0]])

    @staticmethod
    def translate(x, y):
        return np.array([[1, 0, x], [0, 1, y], [0, 0, 1]])

    @staticmethod
    def reflect():
        return np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])

    @staticmethod
    def reflect_x():
        return np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])

    @staticmethod
    def reflect_y():
        return np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])

    @staticmethod
    def orthogonal_projection(x, y):
        factor = np.linalg.norm(np.array([x, y]))**2
        return np.array([[x**2 / factor, x*y / factor, 0], [x*y / factor, y**2 / factor, 0], [0, 0, 1]])

    @staticmethod
    def reflection(x, y):
        factor = np.linalg.norm(np.array([x, y]))**2
        return np.array([[(x**2 - y**2) / factor, 2*x*y / factor, 0], [2*x*y / factor, (y**2 - x**2) / factor, 0], [0, 0, 1]])