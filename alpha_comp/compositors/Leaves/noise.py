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

    def composite(self, index, img):
        if not self.gray:
            self.noise_map = np.floor(np.random.rand(self.width, self.height, 3) ** self.bias * self.limit)
        else:
            self.noise_map = torch.floor(torch.rand(self.width, self.height, device=self.device) ** self.bias * self.limit)
            self.noise_map = self.noise_map.repeat(3, 1, 1).transpose(0, 1).transpose(1, 2)

        mask = torch.zeros((self.width, self.height, 3), device=self.device)
        mask[self.noise_map == index] = 1

        return mask

    def free(self):
        del self.noise_map
