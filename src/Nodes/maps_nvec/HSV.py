import numpy as np
import torch
from src.Nodes.node_socket import NodeSocket
from src.Nodes.node import Node


class HSV(Node):

    def __init__(self, node_id, factory_id):
        self.r = NodeSocket(False, "R", default=None, description="")
        self.g = NodeSocket(False, "G", default=None, description="")
        self.b = NodeSocket(False, "B", default=None, description="")
        super().__init__([self.r, self.g, self.b])

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

    def produce(self):
        mask_h = self.r.get().produce()
        mask_s = self.g.get().produce()
        mask_v = self.b.get().produce()

        H = self._to_hsv(mask_h, self.defaults.width, self.defaults.height)[:, :, 0]
        S = self._to_hsv(mask_s, self.defaults.width, self.defaults.height)[:, :, 1]
        V = self._to_hsv(mask_v, self.defaults.width, self.defaults.height)[:, :, 2]

        out_mask = torch.tensor([H, S, V])

        return out_mask
