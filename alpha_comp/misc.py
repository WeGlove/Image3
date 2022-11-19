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
            return mask, random_array

        return f

    @staticmethod
    def double_func_compose(func_a, func_b, alpha):
        def f(width, height, index, limit, arg):
            mask_a, arg_a = func_a(width, height, index, limit, arg[0] if arg is not None else None)
            mask_b, arg_b = func_b(width, height, index, limit, arg[1] if arg is not None else None)

            mask = numpy.array(mask_a) * alpha + numpy.array(mask_b) * (1 - alpha)
            mask = Image.fromarray(mask)
            mask = mask.convert("L")

            return mask, (arg_a, arg_b)

        return f

    @staticmethod
    def n_func_compose(funcs, alphas):
        def f(width, height, index, limit, arg):
            mask = numpy.array(Image.new("L", (width, height), color=0x00))
            args = []

            for i, (func, alpha) in enumerate(zip(funcs, alphas)):
                mask_f, arg_f = func(width, height, index, limit, None if arg is None else arg[i])
                args.append(arg_f)

                mask = mask + numpy.array(mask_f) * alpha

            mask = Image.fromarray(mask)
            mask = mask.convert("L")

            return mask, args

        return f