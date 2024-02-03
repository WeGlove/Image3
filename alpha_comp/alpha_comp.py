from PIL import Image
import os
import random
from alpha_comp.compositor import Compositor
import numpy as np
from joblib import Parallel, delayed
from typing import Tuple, List


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
    def mass_rep_composition(path, save_path, compositor: Compositor, order="linear", save_masks=None, repeats=1, offset=0):
        def f(i):
            img = AlphaComp.mass_image_compositor(path, compositor, order, save_masks)
            Image.fromarray(np.uint8(img)).save(os.path.join(save_path, f"out_{offset+i}.png"))

        Parallel(n_jobs=-1)(delayed(f)(i) for i in range(repeats))

    @staticmethod
    def production(path, save_path, instruction: List[Tuple[Compositor, int]], order="linear", save_masks=None):
        def f(compositor, repeats, offset):
            AlphaComp.mass_rep_composition(path, save_path, compositor, order, save_masks, repeats, offset)

        counter, counts = 0, []
        for _, repeats in instruction:
            counts.append(counter)
            counter += repeats

        Parallel(n_jobs=-1)(delayed(f)(compositor, repeats, offset) for (compositor, repeats), offset in zip(instruction, counts))
