from typing import List, Tuple
from alpha_comp.compositor import Compositor
import cv2
import torch


class Renderer:

    def __init__(self, fps, device, start_frame=0, stop_frame=-1, repeat=False, display=True):
        self.start_frame = start_frame
        self.stop_frame = stop_frame
        self.fps = fps
        self.repeat = repeat
        self.display = display
        self.device = device

    def run(self, strips: List[Tuple[Compositor, int]], images):
        while True:
            counter = 0
            for compositor, reps in strips:
                compositor.initialize(1080, 1920, len(images), self.device)

                for i in range(reps):
                    if counter < self.start_frame:
                        counter += 1
                        continue
                    if counter >= self.stop_frame and self.stop_frame >= 0:
                        break

                    stack_img = None

                    for i, img in enumerate(images):
                        if stack_img is None:
                            stack_img = torch.zeros(img.shape, device=self.device)

                        mask = compositor.composite(i, img / 255)

                        stack_img = stack_img + torch.multiply(img, mask)

                    if self.display:
                        cv2.imshow('Render', stack_img.cpu().numpy() / 255)
                        if cv2.waitKey(1) == ord('q'):
                            break

                    counter += 1

                compositor.free()

            if not self.repeat:
                break
