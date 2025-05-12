import threading
import time
import cv2
from PIL import Image
import numpy as np
import os
from threading import Lock
import traceback


class Renderer:

    def __init__(self, fps, device, frame_counter, start_frame=0, stop_frame=-1, width=None, height=None, repeat=False, display=True,
                 save=False, save_path="."):
        super().__init__()
        self.start_frame = start_frame
        self.stop_frame = stop_frame
        self.frame_counter = frame_counter
        self.fps = fps
        self.repeat = repeat
        self.display = display
        self.device = device
        self.width = 1920 if width is None else width
        self.height = 1080 if height is None else height
        self.save = save
        self.save_path = save_path

        self.time_error = 0

        self.current_image = None
        self.image_lock = Lock()
        self.run_display_thread = True
        self.new_image = True
        self.current_strip = None

        self.is_paused = True
        self.is_forward = True
        self.is_reset = False
        self.should_reset = False

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

    def _pause(self):
        while self.is_paused:
            time.sleep(1)  # TODO this is terrible

    def _render_thread(self, patch, fps_wait=False):
        while True:
            self.frame_counter.set_frame(0)

            if self.is_paused:
                self._pause()

            self.is_reset = True
            self.should_reset = True

            for frame in range(self.start_frame, self.stop_frame):
                if self.is_paused:
                    self._pause()

                if self.should_reset:
                    self.should_reset = False
                    patch.get_root().initialize(self.width, self.height, [])

                current_frame = self.frame_counter.get()

                self.on_frame(current_frame)

                before_time = time.time()

                if self.is_forward:
                    if current_frame < self.start_frame:
                        self.frame_counter.next()
                        continue
                    if current_frame >= self.stop_frame and self.stop_frame >= 0:
                        break
                else:
                    ...  # TODO

                try:
                    stack_img = patch.get_root().produce()
                except Exception:
                    print(traceback.format_exc())
                    self.pause_unpause()
                    self.reset()
                    break

                if self.is_forward:
                    self.frame_counter.next()
                else:
                    self.frame_counter.previous()

                if self.display:
                    with self.image_lock:
                        self.current_image = stack_img
                        self.new_image = True

                if self.save:
                    mask = Image.fromarray(np.uint8(stack_img.cpu()))
                    mask.save(os.path.join(self.save_path, f"out_{current_frame}.png"))

                delta = time.time() - before_time
                if fps_wait:
                    if 1/self.fps - delta > 0:
                        time.sleep(1/self.fps - delta)
                    else:
                        print("Slow")

            if not self.repeat:
                break

        with self.image_lock:
            self.run_display_thread = False

    def pause_unpause(self):
        self.is_paused = not self.is_paused

    def forwads_backwards(self):
        self.is_forward = not self.is_forward

    def set_frame(self, frame):
        self.frame_counter.set_frame(frame)

    def reset(self):
        self.frame_counter.set_frame(0)
        self.should_reset = True

    def render(self):
        self.save = not self.save

    def set_stopframe(self, frame):
        self.stop_frame = frame

    def repeat_unrepeat(self):
        self.repeat = not self.repeat

    def run(self, node, fps_wait=False):
        self.display_thread = threading.Thread(target=self._display_thread)
        self.display_thread.start()

        self.render_thread = threading.Thread(target=self._render_thread, args=(node, fps_wait))
        self.render_thread.start()

    def join(self):
        self.display_thread.join()
        self.render_thread.join()
