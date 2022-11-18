import numpy
from PIL import Image
import os
import random


class Misc:

    @staticmethod
    def random_mask(seed):
        def f(width, height, index, limit, arg):
            if arg is None:
                rng = numpy.random.default_rng(seed)
                random_array = rng.random((height, width)) * limit
                random_array = numpy.floor(random_array)
            else:
                random_array = arg

            copy = numpy.copy(random_array)
            copy[copy == index] = -1
            copy[copy != -1] = 0
            copy[copy == -1] = 255
            mask = Image.fromarray(copy).convert("L")
            mask.save(f"mask_{index}.png")
            return mask, random_array

        return f