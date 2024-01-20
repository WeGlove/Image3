import numpy as np
from alpha_comp.compositor import Compositor


class TranslationComp(Compositor):

    def __init__(self, compositor, width=0, height=0):
        super().__init__()
        self.compositor = compositor
        self.width_roll = width
        self.height_roll = height

    def initialize(self, width, height, limit):
        super().initialize(width, height, limit)
        self.compositor.initialize(width, height, limit)

    def composite(self, index, img):
        mask = self.compositor.composite(index)
        mask = np.roll(mask, self.width_roll, axis=0)
        mask = np.roll(mask, self.height_roll, axis=1)

        return mask
