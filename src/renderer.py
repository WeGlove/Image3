import logging
import threading
import time
import cv2
from PIL import Image
import numpy as np
import os
from threading import Lock
import traceback
from src.frame_counter import FrameCounter
from src.defaults import Defaults


class Renderer:  # Future TODO Callbacks for exceptions pausing within rednerer!

    def __init__(self, device=None, fps=30, start_frame=0, stop_frame=100000, width=1920, height=1080, repeat=False, display=True,
                 save=False, save_path=".", image_format="png"):
        self.logger = logging.getLogger(__name__)

        self._display_thread = None
        self._render_thread = None

        # Image properties
        self.display = display
        self.save = save
        self.save_path = save_path
        self.new_image = True
        self.current_image = None
        self.image_lock = Lock()
        self.run_display_thread = True
        self.image_format = image_format
        self.defaults = Defaults(width, height, device)

        # Frame Info
        self.start_frame = start_frame
        self.stop_frame = stop_frame
        self.frame_counter = FrameCounter()
        self.fps = fps
        self.is_paused = True
        self.is_forward = True
        self.is_reset = False
        self.should_reset = False
        self.repeat = repeat

        def on_frame(frame, frame_time):
            return frame, frame_time
        self.on_frame = on_frame

    def _wait(self, last_frame_time):
        """
        Wait until 1/fps - (now - before_time) has expired
        :return:
        """
        if time.time() > last_frame_time + 1/self.fps:
            return True
        while True:
            if time.time() > last_frame_time + 1/self.fps:
                break
        return False

    def _display(self):
        """
        The loop that displays new rendered images
        :return:
        """
        last_frame = time.time()
        while self.run_display_thread:
            with self.image_lock:
                render = self.current_image
                is_new = self.new_image
                self.new_image = False

            if render is not None and is_new:
                img = render.cpu().numpy()
                cv2.imshow('Render', img)

                # This is currently necessary to quit because the gui doesn't send signals on quitting
                if cv2.waitKey(1) == ord('q'):
                    break

            self._wait(last_frame)
            last_frame = time.time()

    def _pause(self):
        """
        Wait until unpaused
        :return:
        """
        while self.is_paused:
            time.sleep(1)

    def _render_sequence(self, patch):
        """
        Render a sequence from a patch
        :param patch:
        :return:
        """
        last_frame_time = time.time()
        for frame in range(self.start_frame, self.stop_frame):
            if self.is_paused:
                self._pause()

            if self.should_reset:
                self.should_reset = False
                patch.initialize(self.defaults, [], self.frame_counter)

            current_frame = self.frame_counter.get()
            self.on_frame(current_frame, time.time())  # GUI update

            if self.is_forward:
                if current_frame < self.start_frame:
                    self.frame_counter.next()
                    continue
                if current_frame >= self.stop_frame and self.stop_frame >= 0:
                    break
            else:
                if current_frame < self.start_frame:
                    break
                if current_frame >= self.stop_frame and self.stop_frame >= 0:
                    self.frame_counter.next()
                    continue

            try:
                rendered_img = patch.get_root().produce()
                rendered_img = rendered_img.transpose(0, 1)
                rendered_img = rendered_img % 1
            except Exception:
                self.logger.error(traceback.format_exc())
                self.pause()
                self.reset()
                break

            if self.is_forward:
                self.frame_counter.next()
            else:
                self.frame_counter.previous()

            if self.display:
                with self.image_lock:
                    self.current_image = rendered_img
                    self.new_image = True

            if self.save:
                mask = Image.fromarray(np.uint8(np.clip(rendered_img.cpu() * 255, a_min=0, a_max=255)))
                mask.save(os.path.join(self.save_path, f"render_{current_frame}.{self.image_format}"))
                self.logger.info(f"Saved frame {current_frame}")

            is_slow = self._wait(last_frame_time)
            last_frame_time = time.time()
            if is_slow:
                self.logger.warning(f"Frame {current_frame} was not rendered in time")

    def _render(self, patch):
        """
        The loop rendering new images from a patch
        :param patch:
        :return:
        """
        while True:
            self.frame_counter.set_frame(0)

            if self.is_paused:
                self._pause()

            self.is_reset = True
            self.should_reset = True

            self._render_sequence(patch)

            if not self.repeat:
                break

        with self.image_lock:
            self.run_display_thread = False

    def pause(self):
        """
        Pauses the rendering
        :return:
        """
        self.is_paused = True
        self.logger.info(f"Pause: {self.is_paused}")

    def unpause(self):
        """
        Unpauses the rendering
        :return:
        """
        self.is_paused = False
        self.logger.info(f"Pause: {self.is_paused}")

    def forwards(self):
        """
        Switches to running forwards, unpauses
        :return:
        """
        self.is_forward = True
        self.logger.info(f"Forward: {self.is_forward}")

    def backwards(self):
        """
        Switches to running backwards, unpauses
        :return:
        """
        self.is_forward = False
        self.logger.info(f"Forward: {self.is_forward}")

    def reset(self):
        """
        Reset the patch
        :return:
        """
        self.set_frame(0)
        self.should_reset = True
        self.logger.info("Reset Patch")

    def save_not_save(self):
        """
        Switch between saving and not saving images
        :return:
        """
        self.save = not self.save
        self.logger.info(f"Save: {self.save}")

    def set_frame(self, frame):
        """
        Set the current frame
        :param frame:
        :return:
        """
        self.frame_counter.set_frame(frame)
        self.logger.info(f"Set frame to {frame}")

    def set_stopframe(self, frame):
        """
        Set the last frame
        :param frame:
        :return:
        """
        self.stop_frame = frame
        self.logger.info(f"Set stop frame to {frame}")

    def set_startframe(self, frame):
        """
        Set the last frame
        :param frame:
        :return:
        """
        self.start_frame = frame
        self.logger.info(f"Set start frame to {frame}")

    def set_img_format(self, format: str):
        """
        Set the image format
        :param format:
        :return:
        """
        self.image_format = format

    def set_fps_wait(self, val):
        """
        Set the image format
        :param format:
        :return:
        """
        self.fps_wait = val

    def repeat_unrepeat(self):
        """
        Switch between repeating and not repeating
        """
        self.repeat = not self.repeat
        self.logger.info(f"Repeat {self.repeat}")

    def set_save_path(self, save_path):
        self.save_path = save_path
        self.logger.info(f"Set save path to {save_path}")

    def run(self, patch):
        """
        Run the renderer
        """
        self._display_thread = threading.Thread(target=self._display)
        self._display_thread.start()

        self._render_thread = threading.Thread(target=self._render, args=(patch,))
        self._render_thread.start()

    def join(self):
        """
        Wait until the renderer rejoins.
        :return:
        """
        self._display_thread.join()
        self._render_thread.join()
