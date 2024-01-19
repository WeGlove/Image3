import numpy
from PIL import Image


class VStrips:

    def __init__(self, seed):
        self.seed = seed

    def composite(self, width, height, index, limit, arg):
        if arg is None:
            rng = numpy.random.default_rng(self.seed)
            random_array = rng.random((1, width)) * limit
            random_array = numpy.floor(random_array)
        else:
            random_array = arg

        copy = numpy.copy(random_array)
        copy[copy == index] = -1
        copy[copy != -1] = 0
        copy[copy == -1] = 255

        copy = numpy.repeat(copy, height, axis=0)
        mask = Image.fromarray(copy).convert("L")
        return mask, random_array


class HStrips:

    def __init__(self, seed):
        self.seed = seed

    def composite(self, width, height, index, limit, arg):
        if arg is None:
            rng = numpy.random.default_rng(self.seed)
            random_array = rng.random((height, 1)) * limit
            random_array = numpy.floor(random_array)
        else:
            random_array = arg

        copy = numpy.copy(random_array)
        copy[copy == index] = -1
        copy[copy != -1] = 0
        copy[copy == -1] = 255

        copy = numpy.repeat(copy, width, axis=1)
        mask = Image.fromarray(copy).convert("L")
        return mask, random_array


class Stips:

    def composite(self, width, height, index, limit, arg):
        mask = Image.new("L", (width, height), color=0x00)
        strip = Image.new("L", (round(width / limit), height), color=0xFF)
        mask.paste(strip, (index * round(width / limit), 0, (index + 1) * round(width / limit), height))
        return mask


class StripFade:

    def __init__(self, overlap):
        self.overlap = overlap

    def f(self, width, height, index, limit, arg):
        mask = Image.new("L", (width, height), color=0x00)
        strip = Image.new("L", (round(width / limit), height), color=0xFF)

        left_gradient = Image.new('L', (self.overlap, 1), color=0xFF)
        for x in range(self.overlap):
            left_gradient.putpixel((x, 0), int(255 * x / self.overlap))
        left_alpha = left_gradient.resize((self.overlap, height))

        right_gradient = Image.new('L', (self.overlap, 1), color=0xFF)
        for x in range(self.overlap):
            right_gradient.putpixel((x, 0), int(255 - 255 * x / self.overlap))
        right_alpha = right_gradient.resize((self.overlap, height))

        mask.paste(left_alpha, (index * round(width / limit) - self.overlap, 0, index * round(width / limit), height))
        mask.paste(right_alpha, (index * round(width / limit), 0, index * round(width / limit) + self.overlap, height))

        mask.paste(strip, (index * round(width / limit), 0, (index + 1) * round(width / limit), height))
        return mask, None
