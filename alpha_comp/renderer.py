import time
from typing import List, Tuple
from alpha_comp.compositor import Compositor
from strips.strip import Strip
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
        self.width = 1920
        self.height = 1080

    def run(self, strips: List[Strip], fps_wait=False):
        last_image = torch.zeros((self.width, self.height))

        while True:
            counter = 0
            for strip in strips:
                strip.initialize(self.width, self.height, self.fps, self.start_frame, last_image, self.device)

                for i in range(strip.get_length()):
                    before_time = time.time()

                    if counter < self.start_frame:
                        counter += 1
                        continue
                    if counter >= self.stop_frame and self.stop_frame >= 0:
                        break

                    stack_img = strip.produce(last_image, counter)

                    counter += 1

                    if self.display:
                        cv2.imshow('Render', stack_img.cpu().numpy() / 255)
                        if cv2.waitKey(1) == ord('q'):
                            break

                    delta = time.time() - before_time
                    if fps_wait:
                        if 1/self.fps - delta > 0:
                            time.sleep(1/self.fps - delta)
                        else:
                            print("Slow")

                strip.free()

            if not self.repeat:
                break
