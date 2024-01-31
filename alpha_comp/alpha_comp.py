from PIL import Image
import os
import random
from alpha_comp.compositor import Compositor
import numpy as np


class AlphaComp:

    @staticmethod
    def mass_image_compositor(path, compositor: Compositor, order="linear", save_masks=None):
        dir = os.listdir(path)
        if order == "reverse":
            dir.reverse()
        elif order == "random":
            random.shuffle(dir)
        stack_img = None

        for i, file in enumerate(dir):
            print(f"Compositing {i}")
            img = Image.open(os.path.join(path, file))
            img = np.array(img)
            if stack_img is None:
                stack_img = np.zeros(img.shape)
                compositor.initialize(img.shape[0], img.shape[1], len(dir))
            mask = compositor.composite(i, img / 255)

            stack_img = stack_img + np.multiply(img, mask)

            if save_masks is not None:
                mask = Image.fromarray(np.uint8(np.clip(mask*255, 0, 255)))
                mask.save(os.path.join(save_masks, f"mask_{i}.png"))

        return Image.fromarray(np.uint8(stack_img))

    @staticmethod
    def mass_rep_composition(path, save_path, compositor: Compositor, order="linear", save_masks=None, repeats=1):
        for repeat in range(repeats):
            dir = os.listdir(path)
            if order == "reverse":
                dir.reverse()
            elif order == "random":
                random.shuffle(dir)
            stack_img = None

            for i, file in enumerate(dir):
                print(f"Compositing {i}")
                img = Image.open(os.path.join(path, file))
                img = np.array(img)
                if stack_img is None:
                    stack_img = np.zeros(img.shape)
                    compositor.initialize(img.shape[0], img.shape[1], len(dir))
                mask = compositor.composite(i, img / 255)

                stack_img = stack_img + np.multiply(img, mask)

                if save_masks is not None:
                    mask = Image.fromarray(np.uint8(np.clip(mask*255, 0, 255)))
                    mask.save(os.path.join(save_masks, f"mask_{i}.png"))

            Image.fromarray(np.uint8(stack_img)).save(os.path.join(save_path, f"out_{repeat}.png"))