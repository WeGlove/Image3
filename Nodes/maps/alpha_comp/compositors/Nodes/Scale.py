import itertools
import numpy as np
import torch
from Nodes.maps.alpha_comp.compositor import Compositor


class Scale(Compositor):

    def __init__(self, compositor, scale_x=1, scale_y=1):
        super().__init__()
        self.compositor = compositor
        self.scale_x = scale_x
        self.scale_y = scale_y

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        self.compositor.initialize(width, height, limit)

    def composite(self, index, img):
        mask = np.zeros((self.width, self.height, 3))
        mask_out = self.compositor.composite(index, img)
        for x, y in itertools.product(range(self.width), range(self.height)):
            x_s = x * self.scale_x % self.width
            y_s = y * self.scale_y % self.height
            mask[x, y, :] = mask_out[int(x_s), int(y_s), :]
        return torch.tensor(mask, device=self.device)
