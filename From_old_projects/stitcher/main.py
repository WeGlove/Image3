import math
import os.path
import random

import PIL.ImageOps
from PIL import Image, ImageDraw
import numpy


def strip_mask():
    def f(width, height, index, limit, arg):
        mask = Image.new("L", (width, height), color=0x00)
        strip = Image.new("L", (round(width/limit), height), color=0xFF)
        mask.paste(strip, (index*round(width/limit), 0, (index+1) * round(width/limit), height))
        return mask
    return f


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


def strip_fade_mask(overlap):
    def f(width, height, index, limit, arg):
        mask = Image.new("L", (width, height), color=0x00)
        strip = Image.new("L", (round(width/limit), height), color=0xFF)

        left_gradient = Image.new('L', (overlap, 1), color=0xFF)
        for x in range(overlap):
            left_gradient.putpixel((x, 0), int(255 * x/overlap))
        left_alpha = left_gradient.resize((overlap, height))

        right_gradient = Image.new('L', (overlap, 1), color=0xFF)
        for x in range(overlap):
            right_gradient.putpixel((x, 0), int(255 - 255 * x / overlap))
        right_alpha = right_gradient.resize((overlap, height))

        mask.paste(left_alpha, (index*round(width/limit) - overlap, 0, index * round(width/limit), height))
        mask.paste(right_alpha, (index*round(width/limit), 0, index * round(width/limit) + overlap, height))

        mask.paste(strip, (index*round(width/limit), 0, (index+1) * round(width/limit), height))
        return mask
    return f


def mass_image_compositor(path, out_path, masking_fun, order="linear", save_masks=False):
    dir = os.listdir(path)
    if order == "reverse":
        dir.reverse()
    elif order == "random":
        random.shuffle(dir)
    stack_img = None

    arg = None

    for i, file in enumerate(dir):
        img = Image.open(os.path.join(path, file))
        if stack_img is None:
            stack_img = Image.new("RGBA", img.size, color=0xFF)
        mask, arg = masking_fun(img.width, img.height, i, len(dir), arg)
        img.putalpha(mask)
        stack_img.alpha_composite(img)
        print(f"Composited image {i}")

        if save_masks:
            mask.save(os.path.join(out_path, f"mask_{i}.png"))

    stack_img.save(out_path, "PNG")


if __name__ == '__main__':
    dimensions = (6000, 4000)
    overlap = 1000
    #mass_image_compositor(os.path.join(".", "res", "pear"), f"out_ddd.png", strip_fade_mask(overlap), "random")
    seed = 12345
    mass_image_compositor(os.path.join("../..", "res", "apple"), f"out_ddd.png", random_strip(seed), "random")
