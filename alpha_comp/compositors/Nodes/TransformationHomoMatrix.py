from alpha_comp.Geos import get_homo_vector_map, get_vector_map
import numpy as np
import torch
from strips.animated_property import AnimatedProperty
from alpha_comp.compositor import Compositor


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

        return mask.cuda()

    def get_animated_properties(self, visitors):
        return {visitors + "_TransformationHomoMatrix:mat": self.mat}

    @staticmethod
    def scale(x, y):
        return np.array([[x, 0, 0], [0, y, 0], [0, 0, 1]])

    @staticmethod
    def squeeze(k):
        return TransformationHomoMatrix.scale(k, 1/k)

    @staticmethod
    def shear_x(x):
        return np.array([[1, np.tan(x), 0], [0, 1, 0], [0, 0, 1]])

    @staticmethod
    def shear_y(y):
        return np.array([[1, 0, 0], [np.tan(y), 1, 0], [0, 0, 1]])

    @staticmethod
    def rotation_2D(phi):
        return np.array([[np.cos(phi), -np.sin(phi), 0], [np.sin(phi), np.cos(phi),0 ], [0, 0, 1]])

    @staticmethod
    def perspective_projection_y(y=1):
        return np.array([[1, 0, 0], [0, 1, 0], [0, y, 0]])

    @staticmethod
    def perspective_projection_x(x=1):
        return np.array([[1, 0, 0], [0, 1, 0], [x, 0, 0]])

    @staticmethod
    def translate(x, y):
        return np.array([[1, 0, x], [0, 1, y], [0, 0, 1]])

    @staticmethod
    def reflect():
        return np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])

    @staticmethod
    def reflect_x():
        return np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])

    @staticmethod
    def reflect_y():
        return np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])

    @staticmethod
    def orthogonal_projection(x, y):
        factor = np.linalg.norm(np.array([x, y]))**2
        return np.array([[x**2 / factor, x*y / factor, 0], [x*y / factor, y**2 / factor, 0], [0, 0, 1]])

    @staticmethod
    def reflection(x, y):
        factor = np.linalg.norm(np.array([x, y]))**2
        return np.array([[(x**2 - y**2) / factor, 2*x*y / factor, 0], [2*x*y / factor, (y**2 - x**2) / factor, 0], [0, 0, 1]])