import torch
from alpha_comp.compositor import Compositor
import numpy as np


class Noise(Compositor):
    def __init__(self, gray=True, bias=1):
        super().__init__()
        self.noise_map = None
        self.gray = gray
        self.bias = bias

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        if not self.gray:
            self.noise_map = np.floor(np.random.rand(width, height, 3) ** self.bias * limit)
        else:
            self.noise_map = np.floor(np.random.rand(width, height) ** np.array(self.bias.cpu()) * limit)
            self.noise_map = np.array([self.noise_map, self.noise_map, self.noise_map])
            self.noise_map = np.transpose(self.noise_map, (1, 2, 0))

    def composite(self, index, img):
        mask = np.zeros((self.width, self.height, 3))
        print(mask.shape, self.noise_map.shape)
        mask[self.noise_map == index] = 1

        return torch.tensor(mask, device=self.device)
