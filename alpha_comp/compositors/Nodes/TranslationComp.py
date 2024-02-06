import numpy as np
import torch
from alpha_comp.compositor import Compositor


class TranslationComp(Compositor):

    def __init__(self, compositor, width=0, height=0):
        super().__init__()
        self.compositor = compositor
        self.width_roll = width
        self.height_roll = height

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        self.compositor.initialize(width, height, limit)

    def composite(self, index, img):
        mask = self.compositor.composite(index, img)
        mask = np.roll(mask, self.width_roll, axis=0)
        mask = np.roll(mask, self.height_roll, axis=1)

        return torch.tensor(mask, device=self.device)
