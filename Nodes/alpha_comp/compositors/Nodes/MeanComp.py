import numpy as np
from Nodes.alpha_comp.compositor import Compositor
import torch


class MeanComp(Compositor):

    def __init__(self, compositors):
        super().__init__()
        self.compositors = compositors

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        for compositor in self.compositors:
            compositor.initialize(width, height, limit)

    def composite(self, index, img):
        masks = []
        for compositor in self.compositors:
            mask = compositor.composite(index, img)
            masks.append(mask)

        return torch.tensor(np.mean(masks, axis=0), device=self.device)
