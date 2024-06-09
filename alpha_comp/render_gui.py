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
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QMainWindow, QPushButton


class RenderGui(QMainWindow):

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

        self.setWindowTitle("NightmareMachine")

        button = QPushButton("Pause")

        self.setFixedSize(QSize(400, 300))

        # Set the central widget of the Window.
        self.setCentralWidget(button)

        self.is_paused = False

        def on_pause():
            self.is_paused = not self.is_paused

        button.clicked.connect(on_pause)

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
            counter = 0
            for strip in strips:
                strip.initialize(self.width, self.height, self.fps, self.start_frame, last_image, self.device)

                for i in range(strip.get_length()):
                    while self.is_paused:
                        time.sleep(1)  # TODO this is terrible

                    before_time = time.time()

                    if counter < self.start_frame:
                        counter += 1
                        continue
                    if counter >= self.stop_frame and self.stop_frame >= 0:
                        break

                    print(counter)
                    stack_img = strip.produce(last_image, counter)

                    counter += 1

                    if self.display:
                        with self.image_lock:
                            self.current_image = stack_img
                            self.new_image = True

                    if self.save:
                        mask = Image.fromarray(np.uint8(stack_img.cpu()))
                        mask.save(os.path.join(self.save_path, f"out_{counter}.png"))

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

    def run(self, app, strips: List[Strip], fps_wait=False):
        display_thread = threading.Thread(target=self._display_thread)
        display_thread.start()

        render_thread = threading.Thread(target=self._render_thread, args=(strips, fps_wait))
        render_thread.start()

        self.show()
        app.exec()

        display_thread.join()
        render_thread.join()



