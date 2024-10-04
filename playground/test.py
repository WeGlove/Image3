import os.path
from gui.render_gui import RenderGui
from renderer import Renderer
import torch
from factories import get_misc_factory
from PyQt6.QtWidgets import QApplication
from frame_counter import FrameCounter


if __name__ == "__main__":
    out_path = os.path.join(os.path.join("C:", "Users", "tobia", "Desktop", "out_out"))

    print("cuda", torch.cuda.is_available())

    cuda = torch.device('cuda')

    with ((torch.cuda.device(0))):

        frame_counter = FrameCounter()
        factories = [get_misc_factory(cuda, frame_counter)]

        out = factories[0].instantiate("Output")

        app = QApplication([])
        renderer = Renderer(30, cuda, width=1920, height=1080, start_frame=0, stop_frame=16271, repeat=True,
                            save_path="C:\\Users\\tobia\\Desktop\\out_out", save=False, frame_counter=frame_counter)
        window = RenderGui(renderer, factories, out)

        window.run(app, out, fps_wait=True)
