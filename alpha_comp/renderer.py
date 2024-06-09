import threading
import time
from typing import List
from strips.strip import Strip
import cv2
import torch
from PIL import Image
import numpy as np
import os
from threading import Lock


class Renderer:

    def __init__(self, fps, device, start_frame=0, stop_frame=-1, width=None, height=None, repeat=False, display=True, save=False, save_path="."):
        super().__init__()
        self.start_frame = start_frame
        self.stop_frame = stop_frame
        self.fps = fps
        self.repeat = repeat
        self.display = display
        self.device = device
        self.width = 1920 if width is None else width
        self.height = 1080 if height is None else height
        self.save = save
        self.save_path = save_path

        self.current_image = None
        self.image_lock = Lock()
        self.run_display_thread = True
        self.new_image = True
        self.current_frame = 0
        self.current_strip = None

        self.is_paused = False
        self.is_forward = True

        def on_frame(frame):
            return frame

        self.on_frame = on_frame

    def _display_thread(self):
        while self.run_display_thread:
            a = time.time()
            with self.image_lock:
                render = self.current_image
                is_new = self.new_image
                self.new_image = False
            if render is not None and is_new:
                img = render.cpu().numpy() / 255
                cv2.imshow('Render', img)
                if cv2.waitKey(1) == ord('q'):
                    break

            b = time.time()
            delta = 1 / self.fps - (b - a)
            if delta > 0:
                time.sleep(delta)

    def _render_thread(self, strips: List[Strip], fps_wait=False):
        last_image = torch.zeros((self.width, self.height), device=self.device)

        while True:
            self.current_frame = 0
            for strip in strips:
                strip.initialize(self.width, self.height, self.fps, self.start_frame, last_image, self.device)
                self.current_strip = strip

                for i in range(strip.get_length()):
                    while self.is_paused:
                        time.sleep(1)  # TODO this is terrible

                    self.on_frame(self.current_frame)

                    before_time = time.time()

                    if self.is_forward:
                        if self.current_frame < self.start_frame:
                            self.current_frame += 1
                            continue
                        if self.current_frame >= self.stop_frame and self.stop_frame >= 0:
                            break
                    else:
                        ...  # TODO


                    print(self.current_frame)
                    if self.is_forward:
                        stack_img = strip.produce_next(last_image)
                        self.current_frame += 1
                    else:
                        stack_img = strip.produce_previous(last_image)
                        self.current_frame -= 1

                    if self.display:
                        with self.image_lock:
                            self.current_image = stack_img
                            self.new_image = True

                    if self.save:
                        mask = Image.fromarray(np.uint8(stack_img.cpu()))
                        mask.save(os.path.join(self.save_path, f"out_{self.current_frame}.png"))

                    delta = time.time() - before_time
                    if fps_wait:
                        if 1/self.fps - delta > 0:
                            time.sleep(1/self.fps - delta)
                        else:
                            print("Slow")

                strip.free()

            if not self.repeat:
                break

        with self.image_lock:
            self.run_display_thread = False

    def pause_unpause(self):
        self.is_paused = not self.is_paused

    def forwads_backwards(self):
        self.is_forward = not self.is_forward

    def set_frame(self, frame):
        self.current_frame = frame
        self.current_strip.set_frame(frame)

    def reset(self):
        self.current_frame = 0
        self.current_strip.set_frame(self.current_frame)

    def render(self):
        self.save = not self.save

    def set_stopframe(self, frame):
        self.stop_frame = frame

    def repeat_unrepeat(self):
        self.repeat = not self.repeat

    def run(self, strips: List[Strip], fps_wait=False):
        self.display_thread = threading.Thread(target=self._display_thread)
        self.display_thread.start()

        self.render_thread = threading.Thread(target=self._render_thread, args=(strips, fps_wait))
        self.render_thread.start()

    def join(self):
        self.display_thread.join()
        self.render_thread.join()



