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
            mask, out_arg = compositor.composite(self.width, self.height, index, self.limit, in_arg)
            masks.append(mask)
            out_args.append(out_arg)

        return np.mean(masks, axis=0)
