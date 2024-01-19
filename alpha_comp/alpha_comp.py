from PIL import Image
import os
import random
from typing import List
from compositor import Compositor


class AlphaComp:

    @staticmethod
    def mass_image_compositor(path, compsitors: List[Compositor], order="linear", save_masks=None):
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
            for compositor in compsitors:
                mask, arg = compositor.composite(img.width, img.height, i, len(dir), arg)
            img.putalpha(mask)
            stack_img.alpha_composite(img)
            print(f"Composited image {i}")

            if save_masks is not None:
                mask.save(os.path.join(save_masks, f"mask_{i}.png"))

        return stack_img
