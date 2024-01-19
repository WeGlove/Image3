import numpy as np


class MeanComp:

    def __init__(self, compositors):
        self.compositors = compositors

    def composite(self, width, height, index, limit, arg):
        if arg is None:
            arg = [None] * limit

        out_args = []
        masks = []
        for (compositor, in_arg) in zip(self.compositors, arg):
            mask, out_arg = compositor.composite(width, height, index, limit, in_arg)
            masks.append(mask)
            out_args.append(out_arg)

        return np.mean(masks, axis=0), out_args
