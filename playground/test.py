import os.path
from gui.render_gui import RenderGui
from renderer import Renderer
import torch
from factories import get_map_factory, get_system_factory, get_io_factory, get_math_factory
from PyQt6.QtWidgets import QApplication
from frame_counter import FrameCounter
from patch import Patch


if __name__ == "__main__":
    out_path = os.path.join(os.path.join("C:", "Users", "tobia", "Desktop", "out_out"))

    print("cuda", torch.cuda.is_available())

    cuda = torch.device('cuda')

    with ((torch.cuda.device(0))):

        frame_counter = FrameCounter()
        factories = [get_map_factory(cuda, frame_counter), get_system_factory(cuda, frame_counter),
                     get_io_factory(cuda, frame_counter), get_math_factory(cuda, frame_counter)]

        out = factories[1].instantiate("Output")
        patch = Patch(out)

        app = QApplication([])
        renderer = Renderer(30, cuda, width=1920, height=1080, start_frame=0, stop_frame=16271, repeat=True,
                            save_path="C:\\Users\\tobia\\Desktop\\out_out", save=False, frame_counter=frame_counter)
        window = RenderGui(renderer, factories, patch)

        window.run(app, patch, fps_wait=True)
