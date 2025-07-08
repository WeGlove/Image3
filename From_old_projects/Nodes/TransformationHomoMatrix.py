from src.math.gemoetry import get_homo_vector_map
import torch
from src.Nodes import AnimatedProperty
from src.Nodes import Compositor


class TransformationHomoMatrix(Compositor):

    def __init__(self, compositor, mat):
        super().__init__()
        self.compositor = compositor
        self.mat_original = mat
        self.mat = AnimatedProperty(initial_value=None)

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        self.compositor.initialize(width, height, limit, device)

    def composite(self, index, img):
        self.mat.initial_value = torch.tensor(self.mat_original, device=self.device)
        mask_out = self.compositor.composite(index, img)

        pixel_vectors_center = get_homo_vector_map(self.width, self.height, device=self.device)

        pointers = torch.einsum("tt,ijt->ijt", self.mat.get(), pixel_vectors_center)
        homo_part = pointers[:, :, 2]
        pointers = pointers[:, :, :2]

        pointers[:, :, 0] = (pointers[:, :, 0] / homo_part) % self.width
        pointers[:, :, 1] = (pointers[:, :, 1] / homo_part) % self.height
        pointers = torch.tensor(pointers, dtype=torch.int64)

        pointers_flat = torch.floor(pointers[:, :, 0] * self.height + pointers[:, :, 1])
        pointers_flat = torch.flatten(pointers_flat)

        mask_r = torch.flatten(mask_out[:, :, 0])
        mask_r = mask_r[pointers_flat]
        mask_r = torch.unflatten(mask_r, 0, sizes=(self.width, self.height))

        mask_g = torch.flatten(mask_out[:, :, 1])
        mask_g = mask_g[pointers_flat]
        mask_g = mask_g.reshape((self.width, self.height))

        mask_b = torch.flatten(mask_out[:, :, 2])
        mask_b = mask_b[pointers_flat]
        mask_b = mask_b.reshape((self.width, self.height))

        mask = torch.stack([mask_r, mask_g, mask_b])
        mask = mask.transpose(0, 1).transpose(1, 2)

        return mask

    def get_animated_properties(self, visitors):
        return {visitors + "_TransformationHomoMatrix:mat": self.mat}