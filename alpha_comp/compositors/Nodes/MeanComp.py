import numpy as np
from alpha_comp.compositor import Compositor


class MeanComp(Compositor):

    def __init__(self, compositors):
        super().__init__()
        self.compositors = compositors

    def initialize(self, width, height, limit):
        super().initialize(width, height, limit)
        for compositor in self.compositors:
            compositor.initialize(width, height, limit)

    def composite(self, index):
        masks = []
        for compositor in self.compositors:
            mask = compositor.composite(index)
            masks.append(mask)

        return np.mean(masks, axis=0)
