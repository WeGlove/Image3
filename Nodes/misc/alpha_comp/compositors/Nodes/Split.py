import numpy as np
from Nodes.misc.alpha_comp.compositor import Compositor
import torch


class Split(Compositor):

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
        mask_r = self.compositor_r.composite(index, img)
        mask_g = self.compositor_g.composite(index, img)
        mask_b = self.compositor_b.composite(index, img)

        mask = np.array([mask_r[:, :, 0], mask_g[:, :, 1], mask_b[:, :, 2]])
        mask = np.transpose(mask, (1, 2, 0))

        return torch.tensor(mask, device=self.device)
