import numpy
import torch
from PIL import Image
from alpha_comp.compositor import Compositor


class VStrips(Compositor):

    def __init__(self, seed):
        super().__init__()
        self.seed = seed
        self.random_mask = None

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit)
        self.random_mask = None

    def composite(self, index, img):
        if self.random_mask is None:
            rng = numpy.random.default_rng(self.seed)
            random_array = rng.random((1, self.width)) * self.limit
            random_array = numpy.floor(random_array)
        else:
            random_array = self.random_mask

        copy = numpy.copy(random_array)
        copy[copy == index] = -1
        copy[copy != -1] = 0
        copy[copy == -1] = 255

        copy = numpy.repeat(copy, self.height, axis=0)
        mask = Image.fromarray(copy).convert("L")
        return torch.tensor(mask)


class HStrips(Compositor):

    def __init__(self, seed):
        super().__init__()
        self.seed = seed
        self.random_mask = None

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        self.random_mask = None

    def composite(self, index, img):
        if self.random_mask is None:
            rng = numpy.random.default_rng(self.seed)
            random_array = rng.random((self.height, 1)) * self.limit
            random_array = numpy.floor(random_array)
        else:
            random_array = self.random_mask

        copy = numpy.copy(random_array)
        copy[copy == index] = -1
        copy[copy != -1] = 0
        copy[copy == -1] = 255

        copy = numpy.repeat(copy, self.width, axis=1)

        return copy, random_array


class Strips(Compositor):

    def composite(self, index, img):
        mask = Image.new("L", (self.width, self.height), color=0x00)
        strip = Image.new("L", (round(self.width / self.limit), self.height), color=0xFF)
        mask.paste(strip, (index * round(self.width / self.limit), 0, (index + 1) * round(self.width / self.limit), self.height))
        return torch.tensor(mask, device=self.device)


class StripFade(Compositor):

    def __init__(self, overlap):
        super().__init__()
        self.overlap = overlap

    def f(self, index, img):
        mask = Image.new("L", (self.width, self.height), color=0x00)
        strip = Image.new("L", (round(self.width / self.limit), self.height), color=0xFF)

        left_gradient = Image.new('L', (self.overlap, 1), color=0xFF)
        for x in range(self.overlap):
            left_gradient.putpixel((x, 0), int(255 * x / self.overlap))
        left_alpha = left_gradient.resize((self.overlap, self.height))

        right_gradient = Image.new('L', (self.overlap, 1), color=0xFF)
        for x in range(self.overlap):
            right_gradient.putpixel((x, 0), int(255 - 255 * x / self.overlap))
        right_alpha = right_gradient.resize((self.overlap, self.height))

        mask.paste(left_alpha, (index * round(self.width / self.limit) - self.overlap, 0, index * round(self.width / self.limit), self.height))
        mask.paste(right_alpha, (index * round(self.width / self.limit), 0, index * round(self.width / self.limit) + self.overlap, self.height))

        mask.paste(strip, (index * round(self.width / self.limit), 0, (index + 1) * round(self.width / self.limit), self.height))
        return torch.tensor(mask, device=self.device)
