import numpy as np
from alpha_comp.compositor import Compositor


class Sorting(Compositor):

    def __init__(self, compositor):
        super().__init__()
        self.compositor = compositor
        self.positions_r = None
        self.positions_g = None
        self.positions_b = None

    def initialize(self, width, height, limit):
        super().initialize(width, height, limit)
        self.compositor.initialize(width, height, limit)
        self.positions_r = np.array([0] * height)
        self.positions_g = np.array([0] * height)
        self.positions_b = np.array([0] * height)

    def sort_arr(self, mask, positions):
        out_mask = np.zeros((self.width, self.height))
        row_power = np.sum(mask, axis=0)
        for i in range(self.height):
            power = row_power[i]
            while power > 0 and positions[i] < self.width:
                position = positions[i]
                value = mask[position, i]

                to_fill = 1 - value

                if power < to_fill:
                    out_mask[position, i] = value + power
                    break

                out_mask[position, i] = 1
                positions[i] += 1
                power -= to_fill

        return out_mask, positions

    def composite(self, index, img):
        mask = self.compositor.composite(index)

        out_r = mask[:, :, 0]
        out_r, self.positions_r = self.sort_arr(out_r, self.positions_r)

        out_g = mask[:, :, 1]
        out_g, self.positions_g = self.sort_arr(out_g, self.positions_g)

        out_b = mask[:, :, 2]
        out_b, self.positions_b = self.sort_arr(out_b, self.positions_b)

        out_mask = np.array([out_r, out_g, out_b])
        out_mask = np.transpose(out_mask, (1, 2, 0))

        return out_mask
