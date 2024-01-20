from alpha_comp.compositor import Compositor
import numpy as np
from PIL import Image
import itertools


class Noise(Compositor):
    def __init__(self, gray=True):
        super().__init__()
        self.noise_map = None
        self.gray = gray

    def initialize(self, width, height, limit):
        super().initialize(width, height, limit)
        if not self.gray:
            self.noise_map = np.floor(np.random.rand(width, height, 3) * limit)
        else:
            self.noise_map = np.floor(np.random.rand(width, height) * limit)
            self.noise_map = np.array([self.noise_map, self.noise_map, self.noise_map])
            self.noise_map = np.transpose(self.noise_map, (1, 2, 0))

    def composite(self, index):
        mask = np.zeros((self.width, self.height, 3))
        mask[self.noise_map == index] = 1

        return mask
