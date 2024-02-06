import numpy as np
import torch
from alpha_comp.compositor import Compositor


class SizeSplit(Compositor):

    def __init__(self, compositor_a, compositor_b):
        super().__init__()
        self.compositor_a = compositor_a
        self.compositor_b = compositor_b

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)

        self.compositor_a.initialize(width, height, limit)
        self.compositor_b.initialize(width, height, limit)

    def composite(self, index, img):
        mask_a = self.compositor_a.composite(index, img)
        mask_a = np.floor(mask_a * 255)
        mask_a = np.array(mask_a, dtype=np.int32)
        mask_a = np.mod(mask_a, np.ones((self.width, self.height, 3)) * 0b11110000)

        mask_b = self.compositor_b.composite(index, img)
        mask_b = np.array(np.floor(np.array(np.floor(mask_b * 255), dtype=np.int32) >> 4), dtype=np.int32) << 4

        base_mask = np.array(mask_a + mask_b) / 255
        return torch.tensor(base_mask, device=self.device)
