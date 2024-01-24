import numpy
import numpy as np
from PIL import Image
from alpha_comp.compositor import Compositor


class Closeness(Compositor):

    def __init__(self, comp_img, rev=True):
        super().__init__()
        self.block_mask = None
        self.sizes = []
        self.comp_img = comp_img
        self.rev = rev

    def initialize(self, width, height, limit):
        super().initialize(width, height, limit)
        self.block_mask = np.ones((width, height))
        self.sizes = [width*height//self.limit for _ in range(self.limit)]
        self.sizes[-1] += (width * height) % self.limit

    def composite(self, index, img):
        mask = np.zeros((self.width, self.height))

        brightness = np.mean(np.abs(img - self.comp_img), axis=-1)
        if self.rev:
            brightness = 1 - brightness
        brightness = brightness * self.block_mask
        size = self.sizes[index]
        brightness_sorted = np.flip(np.argsort(brightness.flatten()))
        highest_indices = brightness_sorted[:size]

        mask = mask.flatten()
        mask[highest_indices] = 1
        mask = np.reshape(mask, (self.width, self.height))

        self.block_mask = self.block_mask.flatten()
        self.block_mask[highest_indices] = -1
        self.block_mask = np.reshape(self.block_mask, (self.width, self.height))

        mask = np.array([mask, mask, mask])
        mask = np.transpose(mask, (1, 2, 0))
        return mask

