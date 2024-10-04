import itertools

import numpy as np
import torch

from Nodes.misc.alpha_comp.compositor import Compositor


class TransformationMatrix(Compositor):

    def __init__(self, compositor, mat):
        super().__init__()
        self.compositor = compositor
        self.mat = mat

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        self.compositor.initialize(width, height, limit)

    def composite(self, index, img):
        mask = np.zeros((self.width, self.height, 3))
        mask_out = self.compositor.composite(index, img)
        for x, y in itertools.product(range(self.width), range(self.height)):
            vec = self.mat @ np.array([x, y])
            vec = [int(vec[0] % self.width), int(vec[1] % self.height)]
            mask[x, y, :] = mask_out[vec[0], vec[1], :]
        return torch.tensor(mask, device=self.device)

    @staticmethod
    def scale(x, y):
        return np.array([[x, 0], [0, y]])

    @staticmethod
    def shear_x(phi):
        return np.array([[1, np.tan(phi)], [0, 1]])

    @staticmethod
    def shear_y(phi):
        return np.array([[1, 0], [np.tan(phi), 1]])

    @staticmethod
    def rotation_2D(phi):
        return np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]])