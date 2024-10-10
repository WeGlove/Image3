import numpy as np
from Nodes.maps.alpha_comp.compositor import Compositor
import torch


class SplitImg(Compositor):

    def __init__(self, compositor_r, compositor_g, compositor_b):
        super().__init__()
        self.compositor_r = compositor_r
        self.compositor_g = compositor_g
        self.compositor_b = compositor_b

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        self.compositor_r.initialize(width, height, limit)
        self.compositor_g.initialize(width, height, limit)
        self.compositor_b.initialize(width, height, limit)

    def composite(self, index, img):
        mask_r = self.compositor_r.composite(index,
                                             np.transpose(np.array([img[:, :, 0], img[:, :, 0], img[:, :, 0]]), (1, 2, 0)))
        mask_g = self.compositor_g.composite(index,
                                             np.transpose(np.array([img[:, :, 1], img[:, :, 1], img[:, :, 1]]), (1, 2, 0)))
        mask_b = self.compositor_b.composite(index,
                                             np.transpose(np.array([img[:, :, 2], img[:, :, 2], img[:, :, 2]]), (1, 2, 0)))

        return torch.tensor(np.transpose(np.array([mask_r[:, :, 0], mask_g[:, :, 0], mask_b[:, :, 0]]), (1, 2, 0)), device=self.device)
