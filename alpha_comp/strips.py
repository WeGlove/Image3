import numpy
from PIL import Image
import os
import random


class Strips:

    @staticmethod
    def random_v_strips(seed):
        def f(width, height, index, limit, arg):
            if arg is None:
                rng = numpy.random.default_rng(seed)
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
            mask.save(f"mask_{index}.png")
            return mask, random_array

        return f

    @staticmethod
    def random_h_strips(seed):
        def f(width, height, index, limit, arg):
            if arg is None:
                rng = numpy.random.default_rng(seed)
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
            mask.save(f"mask_{index}.png")
            return mask, random_array

        return f

    @staticmethod
    def strip_mask():
        def f(width, height, index, limit, arg):
            mask = Image.new("L", (width, height), color=0x00)
            strip = Image.new("L", (round(width / limit), height), color=0xFF)
            mask.paste(strip, (index * round(width / limit), 0, (index + 1) * round(width / limit), height))
            return mask

        return f

    @staticmethod
    def strip_fade_mask(overlap):
        def f(width, height, index, limit, arg):
            mask = Image.new("L", (width, height), color=0x00)
            strip = Image.new("L", (round(width / limit), height), color=0xFF)

            left_gradient = Image.new('L', (overlap, 1), color=0xFF)
            for x in range(overlap):
                left_gradient.putpixel((x, 0), int(255 * x / overlap))
            left_alpha = left_gradient.resize((overlap, height))

            right_gradient = Image.new('L', (overlap, 1), color=0xFF)
            for x in range(overlap):
                right_gradient.putpixel((x, 0), int(255 - 255 * x / overlap))
            right_alpha = right_gradient.resize((overlap, height))

            mask.paste(left_alpha, (index * round(width / limit) - overlap, 0, index * round(width / limit), height))
            mask.paste(right_alpha, (index * round(width / limit), 0, index * round(width / limit) + overlap, height))

            mask.paste(strip, (index * round(width / limit), 0, (index + 1) * round(width / limit), height))
            return mask

        return f
