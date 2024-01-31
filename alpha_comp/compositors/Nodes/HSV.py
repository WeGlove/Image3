import time
import numpy as np
from alpha_comp.compositor import Compositor


class HSV(Compositor):

    def __init__(self, compositor_h, compositor_s, compositor_v):
        super().__init__()
        self.compositor_h = compositor_h
        self.compositor_s = compositor_s
        self.compositor_v = compositor_v

    def initialize(self, width, height, limit):
        super().initialize(width, height, limit)
        self.compositor_h.initialize(width, height, limit)
        self.compositor_s.initialize(width, height, limit)
        self.compositor_v.initialize(width, height, limit)

    @staticmethod
    def _to_hsv(mask, width, height):
        min_mask = np.min(mask, axis=-1)
        max_mask = np.max(mask, axis=-1)
        V = max_mask
        delta = max_mask - min_mask

        S = np.zeros((width, height))
        V_pos = V != 0
        S[V_pos] = delta[V_pos] / max_mask[V_pos]

        max_mask_r = max_mask == mask[:, :, 0]
        max_mask_g = max_mask == mask[:, :, 1]
        max_mask_b = max_mask == mask[:, :, 2]

        H = np.zeros((width, height))
        H[max_mask_r] = 60 * (((mask[:, :, 1][max_mask_r] - mask[:, :, 2][max_mask_r]) / delta[max_mask_r]) % 6)
        H[max_mask_g] = 60 * (((mask[:, :, 2][max_mask_g] - mask[:, :, 0][max_mask_g]) / delta[max_mask_g]) + 2)
        H[max_mask_b] = 60 * (((mask[:, :, 0][max_mask_b] - mask[:, :, 1][max_mask_b]) / delta[max_mask_b]) + 4)
        H[delta == 0] = 0
        H = H / 360
        return np.array([H, S, V]).transpose((1, 2, 0))

    def _to_rgb(self, mask):
        H = mask[:, :, 0] * 360
        S = mask[:, :, 1]
        V = mask[:, :, 2]

        C = S * V
        X = C * (1 - np.abs(((H/60) % 2) - 1))
        m = V - C

        out_mask = np.zeros((self.width, self.height, 3))

        out_mask[:, :, 0][300 <= H] = C[300 <= H]
        out_mask[:, :, 2][300 <= H] = X[300 <= H]

        out_mask[:, :, 1][H < 240] = X[H < 240]
        out_mask[:, :, 2][H < 240] = C[H < 240]

        out_mask[:, :, 1][H < 180] = C[H < 180]
        out_mask[:, :, 2][H < 180] = X[H < 180]

        out_mask[:, :, 0][H < 120] = X[H < 120]
        out_mask[:, :, 1][H < 120] = C[H < 120]

        out_mask[:, :, 0][H < 60] = C[H < 60]
        out_mask[:, :, 1][H < 60] = X[H < 60]

        out_mask = out_mask + np.array([m, m, m]).transpose((1, 2, 0))

        return out_mask

    def composite(self, index, img):
        mask_h = self.compositor_h.composite(index, img)
        mask_s = self.compositor_s.composite(index, img)
        mask_v = self.compositor_v.composite(index, img)

        a = time.time()
        H = self._to_hsv(mask_h, self.width, self.height)[:, :, 0]
        S = self._to_hsv(mask_s, self.width, self.height)[:, :, 1]
        V = self._to_hsv(mask_v, self.width, self.height)[:, :, 2]
        print(time.time() - a)

        out_mask = self._to_rgb(np.array([H, S, V]).transpose((1, 2, 0)))

        return out_mask
