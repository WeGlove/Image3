import numpy as np


class TranslationComp:

    def __init__(self, compositor, width=0, height=0):
        self.compositor = compositor
        self.width = width
        self.height = height

    def composite(self, width, height, index, limit, arg):
        mask, out_arg = self.compositor.composite(width, height, index, limit, arg)
        mask = np.roll(mask, self.width, axis=0)
        mask = np.roll(mask, self.height, axis=1)

        return mask, out_arg
